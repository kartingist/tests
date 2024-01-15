from pydantic import BaseModel, Field


class ItemResult(BaseModel):
    id: str
    name: str
    section: str
    description: str
    color: str = None
    price: float = None
    params: str = None


class UploadPhotoItemResponse(BaseModel):
    method: str
    status: str
    result: str


class UploadPhotoItemErrorResponse(BaseModel):
    error: str
    field_error: str
    message: str
    method: str
    status: str
