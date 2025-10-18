from common.schemas.user import (
    UserCreate,
    UserUpdate,
    UserRead,
    ReferralRankCreate,
    ReferralRankUpdate,
    ReferralRankRead,
)
from common.schemas.wallet import (
    CurrencyCreate,
    CurrencyUpdate,
    CurrencyRead,
    WalletCreate,
    WalletUpdate,
    WalletRead,
    TransactionCreate,
    TransactionUpdate,
    TransactionRead,
)
from common.schemas.referral import (
    ReferralCreate,
    ReferralUpdate,
    ReferralRead,
)
from common.schemas.referral_reward import (
    ReferralRewardCreate,
    ReferralRewardUpdate,
    ReferralRewardRead,
)

__all__ = [
    # users/roles/ranks
    "UserCreate",
    "UserUpdate",
    "UserRead",
    "ReferralRankCreate",
    "ReferralRankUpdate",
    "ReferralRankRead",
    # finance
    "CurrencyCreate",
    "CurrencyUpdate",
    "CurrencyRead",
    "WalletCreate",
    "WalletUpdate",
    "WalletRead",
    "TransactionCreate",
    "TransactionUpdate",
    "TransactionRead",
    # referrals
    "ReferralCreate",
    "ReferralUpdate",
    "ReferralRead",
    "ReferralRewardCreate",
    "ReferralRewardUpdate",
    "ReferralRewardRead",
]


