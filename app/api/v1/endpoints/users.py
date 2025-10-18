import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.db.session import get_async_session
from common.models.user import User, ReferralRank
from common.schemas.user import (
    UserCreate,
    UserUpdate,
    UserRead,
    ReferralRankCreate,
    ReferralRankUpdate,
    ReferralRankRead,
)


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserRead])
async def list_users(
    session: AsyncSession = Depends(get_async_session),
    limit: int = 100,
    offset: int = 0,
):
    try:
        result = await session.execute(select(User).offset(offset).limit(limit))
        return result.scalars().all()
    except Exception as exc:
        logger.exception("list_users failed")
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: UUID, session: AsyncSession = Depends(get_async_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(payload: UserCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        db_obj = User(**payload.model_dump())
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    except Exception as exc:
        await session.rollback()
        logger.exception("create_user failed")
        raise HTTPException(status_code=400, detail=str(exc))


@router.patch("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID, payload: UserUpdate, session: AsyncSession = Depends(get_async_session)
):
    db_obj = await session.get(User, user_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    try:
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(db_obj, key, value)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj
    except Exception as exc:
        await session.rollback()
        logger.exception("update_user failed")
        raise HTTPException(status_code=400, detail=str(exc))


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: UUID, session: AsyncSession = Depends(get_async_session)):
    db_obj = await session.get(User, user_id)
    if not db_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    try:
        await session.delete(db_obj)
        await session.commit()
    except Exception as exc:
        await session.rollback()
        logger.exception("delete_user failed")
        raise HTTPException(status_code=400, detail=str(exc))


ranks_router = APIRouter(prefix="/ranks", tags=["ranks"])


@ranks_router.get("/", response_model=List[ReferralRankRead])
async def list_ranks(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(ReferralRank))
        return result.scalars().all()
    except Exception as exc:
        logger.exception("list_ranks failed")
        raise HTTPException(status_code=500, detail=str(exc))


@ranks_router.post("/", response_model=ReferralRankRead, status_code=status.HTTP_201_CREATED)
async def create_rank(
    payload: ReferralRankCreate, session: AsyncSession = Depends(get_async_session)
):
    try:
        rank = ReferralRank(**payload.model_dump())
        session.add(rank)
        await session.commit()
        await session.refresh(rank)
        return rank
    except Exception as exc:
        await session.rollback()
        logger.exception("create_rank failed")
        raise HTTPException(status_code=400, detail=str(exc))


@ranks_router.patch("/{rank_id}", response_model=ReferralRankRead)
async def update_rank(
    rank_id: UUID, payload: ReferralRankUpdate, session: AsyncSession = Depends(get_async_session)
):
    rank = await session.get(ReferralRank, rank_id)
    if not rank:
        raise HTTPException(status_code=404, detail="Rank not found")
    try:
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(rank, k, v)
        await session.commit()
        await session.refresh(rank)
        return rank
    except Exception as exc:
        await session.rollback()
        logger.exception("update_rank failed")
        raise HTTPException(status_code=400, detail=str(exc))


@ranks_router.delete("/{rank_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rank(rank_id: UUID, session: AsyncSession = Depends(get_async_session)):
    rank = await session.get(ReferralRank, rank_id)
    if not rank:
        raise HTTPException(status_code=404, detail="Rank not found")
    try:
        await session.delete(rank)
        await session.commit()
    except Exception as exc:
        await session.rollback()
        logger.exception("delete_rank failed")
        raise HTTPException(status_code=400, detail=str(exc))


