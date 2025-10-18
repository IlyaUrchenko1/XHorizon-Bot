import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.db.session import get_async_session
from common.models.referral import Referral
from common.models.referral_reward import ReferralReward
from common.schemas.referral import ReferralCreate, ReferralUpdate, ReferralRead
from common.schemas.referral_reward import (
    ReferralRewardCreate,
    ReferralRewardUpdate,
    ReferralRewardRead,
)


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/referrals", tags=["referrals"])


@router.get("/", response_model=List[ReferralRead])
async def list_referrals(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(Referral))
        return result.scalars().all()
    except Exception as exc:
        logger.exception("list_referrals failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/", response_model=ReferralRead, status_code=status.HTTP_201_CREATED)
async def create_referral(
    payload: ReferralCreate, session: AsyncSession = Depends(get_async_session)
):
    try:
        obj = Referral(**payload.model_dump())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
    except Exception as exc:
        await session.rollback()
        logger.exception("create_referral failed")
        raise HTTPException(status_code=400, detail=str(exc))


@router.patch("/{referral_id}", response_model=ReferralRead)
async def update_referral(
    referral_id: UUID, payload: ReferralUpdate, session: AsyncSession = Depends(get_async_session)
):
    obj = await session.get(Referral, referral_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Referral not found")
    try:
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        await session.commit()
        await session.refresh(obj)
        return obj
    except Exception as exc:
        await session.rollback()
        logger.exception("update_referral failed")
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/{referral_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_referral(referral_id: UUID, session: AsyncSession = Depends(get_async_session)):
    obj = await session.get(Referral, referral_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Referral not found")
    try:
        await session.delete(obj)
        await session.commit()
    except Exception as exc:
        await session.rollback()
        logger.exception("delete_referral failed")
        raise HTTPException(status_code=400, detail=str(exc))


rewards = APIRouter(prefix="/referral-rewards", tags=["referral-rewards"])


@rewards.get("/", response_model=List[ReferralRewardRead])
async def list_rewards(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(ReferralReward))
        return result.scalars().all()
    except Exception as exc:
        logger.exception("list_rewards failed")
        raise HTTPException(status_code=500, detail=str(exc))


@rewards.post("/", response_model=ReferralRewardRead, status_code=status.HTTP_201_CREATED)
async def create_reward(
    payload: ReferralRewardCreate, session: AsyncSession = Depends(get_async_session)
):
    try:
        obj = ReferralReward(**payload.model_dump())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
    except Exception as exc:
        await session.rollback()
        logger.exception("create_reward failed")
        raise HTTPException(status_code=400, detail=str(exc))


@rewards.patch("/{reward_id}", response_model=ReferralRewardRead)
async def update_reward(
    reward_id: UUID, payload: ReferralRewardUpdate, session: AsyncSession = Depends(get_async_session)
):
    obj = await session.get(ReferralReward, reward_id)
    if not obj:
        raise HTTPException(status_code=404, detail="ReferralReward not found")
    try:
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        await session.commit()
        await session.refresh(obj)
        return obj
    except Exception as exc:
        await session.rollback()
        logger.exception("update_reward failed")
        raise HTTPException(status_code=400, detail=str(exc))


@rewards.delete("/{reward_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reward(reward_id: UUID, session: AsyncSession = Depends(get_async_session)):
    obj = await session.get(ReferralReward, reward_id)
    if not obj:
        raise HTTPException(status_code=404, detail="ReferralReward not found")
    try:
        await session.delete(obj)
        await session.commit()
    except Exception as exc:
        await session.rollback()
        logger.exception("delete_reward failed")
        raise HTTPException(status_code=400, detail=str(exc))


