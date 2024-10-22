from typing import List, Optional
from pydantic import BaseModel


class TimeInterval(BaseModel):
    start_date: str
    end_date: Optional[str] = None

# Shared properties
class WorkflowBase(BaseModel):
    channels: List[str] = None

# Properties to receive via API on creation
class WorkflowCreate(WorkflowBase):
    time_interval: TimeInterval


# Properties to receive via Bussiness on creation
class WorkflowBussinessCreate(WorkflowBase):
    pass

# Properties to receive via API on update
class WorkflowUpdate(WorkflowBase):
    pass

class WorkflowInDBBase(WorkflowBase):
    pass
    class Config:
        pass


class Workflow(BaseModel):
    id: Optional[str] = None


class WorkflowInfo(Workflow):
    pass