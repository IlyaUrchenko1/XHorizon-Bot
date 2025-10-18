
import uuid
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship
from common.db.base import Base

class Referral(Base):
    __tablename__ = "referrals"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    referrer_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False, index=True)
    referee_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False, unique=True, index=True)
    level = sa.Column(sa.Integer, nullable=False)  # 1..10
    path = sa.Column(ARRAY(UUID(as_uuid=True)), nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())

    referrer = relationship("User", foreign_keys=[referrer_id])
    referee = relationship("User", foreign_keys=[referee_id])
