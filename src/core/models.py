from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str
    is_active: bool
    created_at: Optional[datetime] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class StatusResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str


class WordSegmentationRequest(BaseModel):
    text: str


class WordSegmentationResponse(BaseModel):
    original: str
    formatted: str


class ApiResponse(BaseModel):
    message: str
    success: bool = True
    data: Optional[dict] = None
