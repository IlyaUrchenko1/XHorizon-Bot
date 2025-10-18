from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class CurrencyBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code: str = Field(min_length=1, max_length=10)
    decimals: int = 8


class CurrencyCreate(CurrencyBase):
    pass


class CurrencyUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    code: Optional[str] = None
    decimals: Optional[int] = None


class CurrencyRead(CurrencyBase):
    id: UUID


class WalletBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user_id: UUID
    currency_id: UUID
    balance: Optional[float] = 0
    locked_balance: Optional[float] = 0


class WalletCreate(WalletBase):
    pass


class WalletUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    balance: Optional[float] = None
    locked_balance: Optional[float] = None


class WalletRead(WalletBase):
    id: UUID
    created_at: Optional[datetime] = None


class TransactionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    wallet_id: UUID
    type: str
    amount: float
    balance_after: float
    currency_id: Optional[UUID] = None
    status: Optional[str] = "completed"
    meta: Optional[dict] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    type: Optional[str] = None
    amount: Optional[float] = None
    balance_after: Optional[float] = None
    currency_id: Optional[UUID] = None
    status: Optional[str] = None
    meta: Optional[dict] = None


class TransactionRead(TransactionBase):
    id: UUID
    created_at: Optional[datetime] = None


