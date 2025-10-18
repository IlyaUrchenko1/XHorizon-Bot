from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class RegisterRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str
    password: str = Field(min_length=8)
    referral_code: Optional[str] = None
    referrer_id: Optional[str] = None


class TokenRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    id: str
    email: str
    is_active: bool


