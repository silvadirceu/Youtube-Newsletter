from fastapi import APIRouter
from youtube_agent import schemas, business
from typing import Any, List

router = APIRouter()


@router.post("/all-channels", response_model=Any)
async def all_channels(workflow: schemas.WorkflowCreate):
    """
    """
    return await business.workflow.all_channels(workflow)

