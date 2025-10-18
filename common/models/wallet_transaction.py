import uuid
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from common.db.base import Base

class Currency(Base):
    __tablename__ = "currencies"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = sa.Column(sa.String(10), unique=True, nullable=False)
    decimals = sa.Column(sa.Integer, default=8)

class Wallet(Base):
    __tablename__ = "wallets"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False, index=True)
    currency_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("currencies.id"), nullable=False)
    balance = sa.Column(sa.Numeric(20,8), default=0, nullable=False)
    locked_balance = sa.Column(sa.Numeric(20,8), default=0)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

class Transaction(Base):
    __tablename__ = "transactions"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wallet_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("wallets.id"), nullable=False, index=True)
    type = sa.Column(sa.String(64), nullable=False, index=True)
    amount = sa.Column(sa.Numeric(20,8), nullable=False)
    balance_after = sa.Column(sa.Numeric(20,8), nullable=False)
    currency_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("currencies.id"))
    status = sa.Column(sa.String(32), nullable=False, default="completed")
    meta = sa.Column(JSONB, nullable=True)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
