from fastapi import APIRouter
from youtube_agent import schemas, business, workflow_controller
from typing import Any, List

router = APIRouter()


@router.post("/all-channels", response_model=Any)
async def all_channels(workflow: schemas.WorkflowCreate):
    """
    Processes a workflow request for multiple YouTube channels.

    This endpoint receives a workflow containing a list of YouTube channel name or a video link 
    and a time interval. The workflow is processed to retrieve data for all 
    specified channels within the given time range.

    Args:
        workflow (schemas.WorkflowCreate): 
            A workflow object containing the following fields:
            - `channels`: A list of YouTube channel name or a video link.
            - `time_interval`: An object specifying:
                - `start_date` (str): The start of the time range, formatted as `YYYY-MM-DDTHH:MM:SSZ`.
                - `end_date` (Optional[str]): The end of the time range, formatted as `YYYY-MM-DDTHH:MM:SSZ`. This field is optional; if not provided, data will be retrieved up to the present moment.

    """
    return await workflow_controller.workflow.all_channels(workflow)

