from fastapi import APIRouter
from youtube_agent import schemas, business, workflow_controller
from typing import Any, List

router = APIRouter()


@router.post("/all-channels", response_model=Any)
async def all_channels(workflow: schemas.WorkflowCreate):
    """
    """
    return await workflow_controller.workflow.all_channels(workflow)

