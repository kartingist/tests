from pydantic import BaseModel, Field


class GetItemResult(BaseModel):
    id: str
    name: str
    section: str
    description: str
    color: str = None
    price: float = None
    params: str = None
    photo: str = None


class GetItemResponse(BaseModel):
    method: str
    status: str
    result: GetItemResult


class GetItemErrorResponse(BaseModel):
    error: str
    field_error: str
    message: str
    method: str
    status: str
