from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ReferralRewardBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: UUID
    from_user_id: UUID
    level: int
    amount: float
    currency_id: Optional[UUID] = None
    status: str = "pending"
    source_tx_id: Optional[UUID] = None


class ReferralRewardCreate(ReferralRewardBase):
    pass


class ReferralRewardUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    level: Optional[int] = None
    amount: Optional[float] = None
    currency_id: Optional[UUID] = None
    status: Optional[str] = None
    source_tx_id: Optional[UUID] = None


class ReferralRewardRead(ReferralRewardBase):
    id: UUID
    created_at: Optional[datetime] = None


