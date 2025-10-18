from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class ReferralRankBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str = Field(min_length=1, max_length=64)
    personal_deposit_min: Optional[float] = 0
    team_turnover_min: Optional[float] = 0
    income_structure: dict = Field(default_factory=dict)
    max_depth: int = 3


class ReferralRankCreate(ReferralRankBase):
    pass


class ReferralRankUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: Optional[str] = None
    personal_deposit_min: Optional[float] = None
    team_turnover_min: Optional[float] = None
    income_structure: Optional[dict] = None
    max_depth: Optional[int] = None


class ReferralRankRead(ReferralRankBase):
    id: UUID


class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: str
    is_active: Optional[bool] = True
    referral_code: str
    referrer_id: Optional[UUID] = None
    rank_id: Optional[UUID] = None
    personal_deposit_sum: Optional[float] = 0
    team_turnover: Optional[float] = 0


class UserCreate(UserBase):
    password_hash: str


class UserUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    email: Optional[str] = None
    password_hash: Optional[str] = None
    is_active: Optional[bool] = None
    referral_code: Optional[str] = None
    referrer_id: Optional[UUID] = None
    rank_id: Optional[UUID] = None
    personal_deposit_sum: Optional[float] = None
    team_turnover: Optional[float] = None


class UserRead(UserBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


