from pydantic import BaseModel, Field


class ItemResult(BaseModel):
    id: str
    name: str
    section: str
    description: str
    color: str = None
    price: float = None
    params: str = None


class UpdateItemResponse(BaseModel):
    method: str
    status: str
    result: str


class UpdateItemErrorResponse(BaseModel):
    error: str
    field_error: str
    message: str
    method: str
    status: str
