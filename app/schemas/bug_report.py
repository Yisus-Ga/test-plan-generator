from pydantic import BaseModel


class BugReportRequest(BaseModel):
    test_plan_id: int
    descripcion_informal: str


class BugReportResponse(BaseModel):
    content: str
