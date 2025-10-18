"""initial schema without roles

Revision ID: 20251018_000001
Revises: 
Create Date: 2025-10-18 00:00:01

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '20251018_000001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # referral_ranks
    op.create_table(
        'referral_ranks',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('name', sa.String(length=64), nullable=False, unique=True),
        sa.Column('personal_deposit_min', sa.Numeric(20, 8), server_default='0', nullable=True),
        sa.Column('team_turnover_min', sa.Numeric(20, 8), server_default='0', nullable=True),
        sa.Column('income_structure', postgresql.JSONB(astext_type=sa.Text()), server_default='{}', nullable=False),
        sa.Column('max_depth', sa.Integer(), server_default='3', nullable=True),
    )

    # users
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('password_hash', sa.Text(), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=True),
        sa.Column('referral_code', sa.String(length=64), nullable=False),
        sa.Column('referrer_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('rank_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('personal_deposit_sum', sa.Numeric(20, 8), server_default='0', nullable=True),
        sa.Column('team_turnover', sa.Numeric(20, 8), server_default='0', nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['referrer_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['rank_id'], ['referral_ranks.id'], ),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('referral_code'),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=False)
    op.create_index('ix_users_referrer_id', 'users', ['referrer_id'], unique=False)

    # currencies
    op.create_table(
        'currencies',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('code', sa.String(length=10), nullable=False),
        sa.Column('decimals', sa.Integer(), server_default='8', nullable=True),
        sa.UniqueConstraint('code'),
    )

    # wallets
    op.create_table(
        'wallets',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('currency_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('balance', sa.Numeric(20, 8), server_default='0', nullable=False),
        sa.Column('locked_balance', sa.Numeric(20, 8), server_default='0', nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ),
    )
    op.create_index('ix_wallets_user_id', 'wallets', ['user_id'], unique=False)

    # transactions
    op.create_table(
        'transactions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('wallet_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('type', sa.String(length=64), nullable=False),
        sa.Column('amount', sa.Numeric(20, 8), nullable=False),
        sa.Column('balance_after', sa.Numeric(20, 8), nullable=False),
        sa.Column('currency_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('status', sa.String(length=32), server_default='completed', nullable=False),
        sa.Column('meta', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['wallet_id'], ['wallets.id'], ),
        sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ),
    )
    op.create_index('ix_transactions_wallet_id', 'transactions', ['wallet_id'], unique=False)
    op.create_index('ix_transactions_type', 'transactions', ['type'], unique=False)

    # referrals
    op.create_table(
        'referrals',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('referrer_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('referee_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('path', postgresql.ARRAY(postgresql.UUID(as_uuid=True)), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['referrer_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['referee_id'], ['users.id'], ),
        sa.UniqueConstraint('referee_id'),
    )
    op.create_index('ix_referrals_referrer_id', 'referrals', ['referrer_id'], unique=False)
    op.create_index('ix_referrals_referee_id', 'referrals', ['referee_id'], unique=True)

    # referral_rewards
    op.create_table(
        'referral_rewards',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('from_user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Numeric(20, 8), nullable=False),
        sa.Column('currency_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('status', sa.String(length=32), server_default='pending', nullable=True),
        sa.Column('source_tx_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['from_user_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['currency_id'], ['currencies.id'], ),
        sa.ForeignKeyConstraint(['source_tx_id'], ['transactions.id'], ),
    )
    op.create_index('ix_referral_rewards_user_id', 'referral_rewards', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_referral_rewards_user_id', table_name='referral_rewards')
    op.drop_table('referral_rewards')

    op.drop_index('ix_referrals_referee_id', table_name='referrals')
    op.drop_index('ix_referrals_referrer_id', table_name='referrals')
    op.drop_table('referrals')

    op.drop_index('ix_transactions_type', table_name='transactions')
    op.drop_index('ix_transactions_wallet_id', table_name='transactions')
    op.drop_table('transactions')

    op.drop_index('ix_wallets_user_id', table_name='wallets')
    op.drop_table('wallets')

    op.drop_table('currencies')

    op.drop_index('ix_users_referrer_id', table_name='users')
    op.drop_index('ix_users_email', table_name='users')
    op.drop_table('users')

    op.drop_table('referral_ranks')


