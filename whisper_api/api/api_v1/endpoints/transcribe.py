from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from innocore import models, schemas, business
from pyfox.connectors.sql_app import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Chatbot])
def get_multi(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(business.get_current_active_user),
) -> Any:
    """
    Retrieve Chabots by user.
    """
    return business.chatbot.get_multi(db, current_user)


@router.get("/get/{id}", response_model=schemas.Chatbot)
def get(
    id: int,
    current_user: models.User = Depends(business.get_current_active_user),
    db: Session = Depends(get_db),
) -> Any:
    """
    Get a specific chabtot by id.
    """
    chatbot = business.chatbot.get(db, id, current_user)
    if not chatbot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Chatbot não encontrado"
        )
    return chatbot


@router.post("/", response_model=schemas.Chatbot)
def post(
    obj_in: schemas.ChatbotCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(business.get_current_active_user),
) -> Any:
    """
    Create new chatbot
    """
    return business.chatbot.create(db, obj_in, current_user)


@router.put("/{id}", response_model=schemas.Chatbot)
def update(
    *,
    db: Session = Depends(get_db),
    id: int,
    obj_in: schemas.ChatbotUpdate,
    current_user: models.User = Depends(business.get_current_active_user),
) -> Any:
    """
    Update a Chatbot.
    """
    return business.chatbot.update(db, id, obj_in, current_user)


@router.delete("/{id}", response_model=schemas.Chatbot)
def delete(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: models.User = Depends(business.get_current_active_user),
) -> Any:
    """
    Remove a Chatbot.
    """
    return business.chatbot.remove(db, id, current_user)
