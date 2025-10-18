import uuid
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from common.db.base import Base

class ReferralReward(Base):
    __tablename__ = "referral_rewards"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False, index=True)
    from_user_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False)
    level = sa.Column(sa.Integer, nullable=False)
    amount = sa.Column(sa.Numeric(20,8), nullable=False)
    currency_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("currencies.id"))
    status = sa.Column(sa.String(32), default="pending")
    source_tx_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("transactions.id"))
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
