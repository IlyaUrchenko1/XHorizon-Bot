import uuid
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from sqlalchemy.orm import relationship
from common.db.base import Base

class ReferralRank(Base):
    __tablename__ = "referral_ranks"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.String(64), unique=True, nullable=False)
    personal_deposit_min = sa.Column(sa.Numeric(20,8), default=0)
    team_turnover_min = sa.Column(sa.Numeric(20,8), default=0)
    income_structure = sa.Column(JSONB, nullable=False, server_default='{}')
    max_depth = sa.Column(sa.Integer, default=3)

class User(Base):
    __tablename__ = "users"
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = sa.Column(sa.String(320), unique=True, nullable=False, index=True)
    password_hash = sa.Column(sa.Text, nullable=False)
    is_active = sa.Column(sa.Boolean, default=True)
    referral_code = sa.Column(sa.String(64), unique=True, nullable=False)
    referrer_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=True, index=True)
    rank_id = sa.Column(UUID(as_uuid=True), sa.ForeignKey("referral_ranks.id"), nullable=True)
    personal_deposit_sum = sa.Column(sa.Numeric(20,8), default=0)
    team_turnover = sa.Column(sa.Numeric(20,8), default=0)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    updated_at = sa.Column(sa.DateTime(timezone=True), onupdate=sa.func.now())

    rank = relationship("ReferralRank")
    referrer = relationship("User", remote_side=[id], backref="referees")
