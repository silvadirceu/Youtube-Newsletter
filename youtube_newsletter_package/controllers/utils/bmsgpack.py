"""Module for converting objects to msgpack bytes and vice versa."""

import msgpack
import msgpack_numpy as m

m.patch()


def object_to_dict(obj):
    if isinstance(obj, list):
        return [object_to_dict(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: object_to_dict(v) for k, v in obj.items()}
    elif hasattr(obj, "__dict__"):
        return object_to_dict(obj.__dict__)
    else:
        return obj


def obj_to_msgpack(obj):
    """Convert an object to msgpack bytes."""
    return msgpack.packb(obj)


def msgpack_to_obj(bytes):
    """Convert msgpack bytes to an object."""
    return msgpack.unpackb(bytes)
