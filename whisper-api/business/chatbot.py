from typing import List

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from innocore import crud, models, schemas
from pyfox.connectors.db.businessbase import BusinessBase


class BusinessChatbot(
    BusinessBase[
        models.User,
        crud.CRUDChatbot,
        models.Chatbot,
        schemas.ChatbotCreate,
        schemas.ChatbotUpdate,
    ]
):
    def get_multi(self, db: Session, current_user: models.User) -> List[models.Chatbot]:
        """
        Returns all objects.
        """
        return self.crud.get_by_key_value(db, "owner_id", current_user.id)

    def get(self, db: Session, id: int, current_user: models.User) -> models.Chatbot:
        """
        Returns an object.
        """
        obj = self.crud.get(db, id)
        if not current_user.id == obj.owner_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Operação não permitida para este usuário",
            )
        return obj

    def remove(
        self, db: Session, obj_id: int, current_user: models.User
    ) -> models.Chatbot:
        """
        Deletes an object.
        """
        if not self.user_can_remove(db, current_user, obj_id):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Operação não permitida para este usuário",
            )
        return self.crud.remove(db, id=obj_id)

    def create(
        self, db: Session, obj_in: schemas.ChatbotCreate, current_user: models.User
    ) -> models.Chatbot:
        """
        Creates an chatbot.
        """
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["owner_id"] = current_user.id
        crud_obj = schemas.ChatbotBussinessCreate(**obj_in_data)  # type: ignore
        return self.crud.create(db, obj_in=crud_obj)

    def user_can_update(
        self,
        db: Session,
        user: models.User,
        obj_in: schemas.ChatbotUpdate,
        obj: models.Chatbot,
    ) -> bool:
        if not user.id == obj.owner_id:
            return False
        return True

    def user_can_remove(self, db: Session, user: models.User, obj_id: int) -> bool:
        chatbot = self.get(db, obj_id, user)
        if not chatbot.owner_id == user.id:
            return False
        return True


chatbot = BusinessChatbot(crud.chatbot)
