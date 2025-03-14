from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class ModerationRequest(BaseModel):
    content: str
    content_type: str = Field(..., description="Type of content: 'text' or 'image'")
    metadata: Optional[Dict[str, Any]] = None


class ModerationResult(BaseModel):
    content_type: str
    category: str
    confidence: float
    is_flagged: bool
    text_analysis: Optional[Dict[str, Any]] = None


class ModerationResponse(BaseModel):
    content_hash: str
    moderation_result: ModerationResult
    blockchain_transaction: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ModerationHistory(BaseModel):
    content_hash: str
    history: List[ModerationResult]
