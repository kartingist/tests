from pydantic import BaseModel, Field


class ItemResult(BaseModel):
    id: str
    name: str
    section: str
    description: str
    color: str = None
    price: float = None
    params: str = None


class CreateItemResponse(BaseModel):
    method: str
    status: str
    result: ItemResult


class CreateItemErrorResponse(BaseModel):
    error: str
    field_error: str
    message: str
    method: str
    status: str
