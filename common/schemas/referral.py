from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ReferralBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    referrer_id: UUID
    referee_id: UUID
    level: int
    path: List[UUID]


class ReferralCreate(ReferralBase):
    pass


class ReferralUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    level: Optional[int] = None
    path: Optional[List[UUID]] = None


class ReferralRead(ReferralBase):
    id: UUID
    created_at: Optional[datetime] = None


