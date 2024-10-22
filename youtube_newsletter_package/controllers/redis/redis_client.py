from typing import Any, Awaitable, List, Union
import redis
import uuid
import msgpack
import datetime
from ..utils.bmsgpack import obj_to_msgpack, msgpack_to_obj, object_to_dict
from ..settings.redis_settings import RedisSettings

SHARD_KEY = "shard:"
SHARD_BLOCK_KEY = "shard:block:"
SHARD_SIZE = 314572800  # 300 MB


class RedisClient:
    """Redis Client."""

    def __init__(self) -> None:
        """
        Initialize a new instance of the RedisClient class.

        Parameters:
        redis_url (str): The URL of the Redis server to connect to.
        """
        settings = RedisSettings()
        self.redis = redis.from_url(str(settings.REDIS_DATABASE_URI))
        self.shard_size = settings.SHARD_SIZE

    def split_in_chunks(self, array, n):
        """
        Yield successive n-sized chunks from array.

        Parameters:
        array (list): The list to split into chunks.
        n (int): The size of each chunk.

        Yields:
        list: The next chunk of the array.
        """
        for i in range(0, len(array), n):
            yield array[i : i + n]

    def shard_block(self, obj, chunk_size: int = None):
        """
        Shard a block of data into chunks and store them in Redis.

        Parameters:
        obj (object): The data to shard.
        chunk_size (int, optional): The size of each chunk. Defaults to None.

        Returns:
        tuple: The ID of the shard and the result of setting the primary value.
        """
        if chunk_size is None:
            chunk_size = self.shard_size
        packed_data = msgpack.packb(obj)
        chunks = self.split_in_chunks(packed_data, chunk_size)
        keys = []
        for chunk in chunks:
            key = str(uuid.uuid1())
            keys.append(key)
            self.set_primary_value(key=SHARD_BLOCK_KEY + key, value=chunk)

        shard_id = str(uuid.uuid1())
        key = SHARD_KEY + shard_id
        return shard_id, self.set_primary_value(key=key, value=keys)

    def unshard_block(self, shard_id):
        """
        Unshard a block of data from chunks stored in Redis.

        Parameters:
        shard_id (str): The ID of the shard to unshard.

        Returns:
        object: The unsharded data.
        """
        key = SHARD_KEY + shard_id
        keys = self.get_primary_value(key)
        chunks = []
        for k in keys:
            chunks.append(self.get_primary_value(SHARD_BLOCK_KEY + k))
        packed_data = b"".join(chunks)
        return msgpack.unpackb(packed_data)

    def get_primary_value(self, key: str) -> Any:
        """Get the value of a key."""
        packed = self.redis.get(key)
        return None if packed is None else msgpack.unpackb(packed)

    def set_primary_value(self, key: str, value: Any, ttl: int = 172800) -> bool:
        """
        Set the value of a key in Redis with a TTL (Time To Live) of 172800 seconds (48 hours).

        The value is packed into a binary format using MessagePack before being stored.

        Parameters:
        key (str): The key to set.
        value (any): The value to set. This can be any type that is serializable by MessagePack.

        Returns:
        bool: True if the operation was successful, False otherwise.
        """
        packed_data: bytes = msgpack.packb(value)
        self.redis.setex(key, ttl, packed_data)
        return bool(self.redis.setex(key, ttl, packed_data))

    def delete_primary_value(self, key: str) -> Awaitable[int]:
        """
        Asynchronously delete the value associated with a given key in Redis.

        This function takes a key as an argument and deletes the corresponding value in Redis.
        It is an asynchronous function and returns a future integer that represents
        the number of keys that were removed.

        Parameters:
        key (str): The key of the value to delete in Redis.

        Returns:
        Awaitable[int]: A future that represents the number of keys that were removed.
        """
        return self.redis.delete(key)

    def set_data(self, data: Any, ttl: int = 30000) -> str:
        """
        Set the data to be consumed by the workers.

        This function takes a dict object, converts it to MessagePack format,
        shards it, and stores it in Redis with a unique key. The key is then returned.

        Parameters:
        data (dict): The data to be consumed by the workers.

        Returns:
        str: The key under which the data is stored in Redis.
        """
        key = str(uuid.uuid4())
        data_dict = object_to_dict(data)
        shard_id, _ = self.shard_block(obj_to_msgpack(data_dict))
        self.set_primary_value(key, shard_id, ttl)
        return key

    def get_data(self, key: str) -> Any:
        """
        Get the data to be consumed by the workers.

        This function takes a key, retrieves the corresponding shard ID from Redis,
        unshards it.

        Parameters:
        key (str): The key under which the data is stored in Redis.

        Returns:
        Any: The data to be consumed by the workers, if the redis key id is found.
        ValueError: If no shard ID is associated with the key.
        """
        shard_id = self.get_primary_value(key)
        if not shard_id:
            print(f"No shard ID associated with the key: {key}")
            raise ValueError("Task data not found in Redis")
        data = self.unshard_block(shard_id)
        deserialized_data = msgpack_to_obj(data)
        return deserialized_data

    def update_data(
        self, shard_key: str, dict_keys: str, value: Any, ttl: int = 30000
    ) -> bool:
        """
        Update a value in the dictionary stored at the given shard key in Redis.

        Parameters:
        shard_key (str): The shard key under which the dictionary is stored in Redis.
        dict_keys (List[str]): The keys in the dictionary to update. Can be nested keys, with levels separated by '.'.
        value (Any): The new value to set.

        Returns:
        bool: True if the update was successful, False otherwise.
        """

        data = self.get_data(shard_key)

        if not data:
            print(f"No data associated with the key: {shard_key}")
            return False

        # Split the dict_keys by '.' and get the last key
        keys = dict_keys.split(".")
        last_key = keys.pop()

        # Convert the data object to a dictionary
        data_dict = object_to_dict(data)

        # Traverse the dictionary using the keys
        temp = data_dict
        for key in keys:
            temp = temp.get(key, {})

        # Set the value at the last key
        temp[last_key] = value

        # Delete and re-shard the updated data
        self.delete_data(shard_key)
        shard_id, _ = self.shard_block(obj_to_msgpack(data_dict))
        return self.set_primary_value(shard_key, shard_id, ttl)

    def delete_data(self, key: str) -> bool:
        """
        Delete the data associated with a given key in Redis, which is meant to be consumed by workers.

        Parameters:
        key (str): The key of the data to delete in Redis.

        Returns:
        bool: True if all operations were successful, False otherwise.
        """
        # Step 1: Retrieve the shard ID using the generated key.
        shard_id = self.get_primary_value(key)
        if not shard_id:
            print(f"No shard ID associated with the key: {key}")
            return False

        # Step 2: Retrieve all the chunk keys associated with the shard ID.
        shard_key = SHARD_KEY + shard_id
        chunk_keys = self.get_primary_value(shard_key)
        if not chunk_keys:
            print(f"No chunk keys associated with the shard ID: {shard_key}")
            return False
        # Step 3: Delete all the chunk keys.
        for chunk_key in chunk_keys:
            deleted = self.delete_primary_value(SHARD_BLOCK_KEY + chunk_key)
            if not deleted:
                print(f"Failed to delete chunk key: {SHARD_BLOCK_KEY + chunk_key}")

        # Step 4: Delete the shard ID.
        if not self.delete_primary_value(shard_key):
            print(f"Failed to delete shard key: {shard_key}")

        # Step 5: Delete the generated key.
        if not self.delete_primary_value(key):
            print(f"Failed to delete main key: {key}")
            return False

        return True
