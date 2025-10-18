import logging
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from common.db.session import get_async_session
from common.models.wallet_transaction import Currency, Wallet, Transaction
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


logger = logging.getLogger(__name__)

currencies = APIRouter(prefix="/currencies", tags=["currencies"])


@currencies.get("/", response_model=List[CurrencyRead])
async def list_currencies(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(Currency))
        return result.scalars().all()
    except Exception as exc:
        logger.exception("list_currencies failed")
        raise HTTPException(status_code=500, detail=str(exc))


@currencies.post("/", response_model=CurrencyRead, status_code=status.HTTP_201_CREATED)
async def create_currency(
    payload: CurrencyCreate, session: AsyncSession = Depends(get_async_session)
):
    try:
        obj = Currency(**payload.model_dump())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
    except Exception as exc:
        await session.rollback()
        logger.exception("create_currency failed")
        raise HTTPException(status_code=400, detail=str(exc))


@currencies.patch("/{currency_id}", response_model=CurrencyRead)
async def update_currency(
    currency_id: UUID,
    payload: CurrencyUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    obj = await session.get(Currency, currency_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Currency not found")
    try:
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        await session.commit()
        await session.refresh(obj)
        return obj
    except Exception as exc:
        await session.rollback()
        logger.exception("update_currency failed")
        raise HTTPException(status_code=400, detail=str(exc))


@currencies.delete("/{currency_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_currency(currency_id: UUID, session: AsyncSession = Depends(get_async_session)):
    obj = await session.get(Currency, currency_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Currency not found")
    try:
        await session.delete(obj)
        await session.commit()
    except Exception as exc:
        await session.rollback()
        logger.exception("delete_currency failed")
        raise HTTPException(status_code=400, detail=str(exc))


wallets = APIRouter(prefix="/wallets", tags=["wallets"])


@wallets.get("/", response_model=List[WalletRead])
async def list_wallets(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(Wallet))
        return result.scalars().all()
    except Exception as exc:
        logger.exception("list_wallets failed")
        raise HTTPException(status_code=500, detail=str(exc))


@wallets.post("/", response_model=WalletRead, status_code=status.HTTP_201_CREATED)
async def create_wallet(payload: WalletCreate, session: AsyncSession = Depends(get_async_session)):
    try:
        obj = Wallet(**payload.model_dump())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
    except Exception as exc:
        await session.rollback()
        logger.exception("create_wallet failed")
        raise HTTPException(status_code=400, detail=str(exc))


@wallets.patch("/{wallet_id}", response_model=WalletRead)
async def update_wallet(
    wallet_id: UUID, payload: WalletUpdate, session: AsyncSession = Depends(get_async_session)
):
    obj = await session.get(Wallet, wallet_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Wallet not found")
    try:
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        await session.commit()
        await session.refresh(obj)
        return obj
    except Exception as exc:
        await session.rollback()
        logger.exception("update_wallet failed")
        raise HTTPException(status_code=400, detail=str(exc))


@wallets.delete("/{wallet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_wallet(wallet_id: UUID, session: AsyncSession = Depends(get_async_session)):
    obj = await session.get(Wallet, wallet_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Wallet not found")
    try:
        await session.delete(obj)
        await session.commit()
    except Exception as exc:
        await session.rollback()
        logger.exception("delete_wallet failed")
        raise HTTPException(status_code=400, detail=str(exc))


transactions = APIRouter(prefix="/transactions", tags=["transactions"])


@transactions.get("/", response_model=List[TransactionRead])
async def list_transactions(session: AsyncSession = Depends(get_async_session)):
    try:
        result = await session.execute(select(Transaction))
        return result.scalars().all()
    except Exception as exc:
        logger.exception("list_transactions failed")
        raise HTTPException(status_code=500, detail=str(exc))


@transactions.post("/", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    payload: TransactionCreate, session: AsyncSession = Depends(get_async_session)
):
    try:
        obj = Transaction(**payload.model_dump())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
    except Exception as exc:
        await session.rollback()
        logger.exception("create_transaction failed")
        raise HTTPException(status_code=400, detail=str(exc))


@transactions.patch("/{tx_id}", response_model=TransactionRead)
async def update_transaction(
    tx_id: UUID, payload: TransactionUpdate, session: AsyncSession = Depends(get_async_session)
):
    obj = await session.get(Transaction, tx_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Transaction not found")
    try:
        for k, v in payload.model_dump(exclude_unset=True).items():
            setattr(obj, k, v)
        await session.commit()
        await session.refresh(obj)
        return obj
    except Exception as exc:
        await session.rollback()
        logger.exception("update_transaction failed")
        raise HTTPException(status_code=400, detail=str(exc))


@transactions.delete("/{tx_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(tx_id: UUID, session: AsyncSession = Depends(get_async_session)):
    obj = await session.get(Transaction, tx_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Transaction not found")
    try:
        await session.delete(obj)
        await session.commit()
    except Exception as exc:
        await session.rollback()
        logger.exception("delete_transaction failed")
        raise HTTPException(status_code=400, detail=str(exc))


