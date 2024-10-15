from fastapi import APIRouter
from youtube_agent import schemas, business
from typing import Any, List

router = APIRouter()


@router.post("/workflow-all-channels", response_model=Any)
async def workflow_all_channels(workflow: schemas.WorkflowCreate):
    """
    """
    return await business.workflow.workflow_all_channels(workflow)

