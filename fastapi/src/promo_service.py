from datetime import datetime
from functools import lru_cache
from uuid import UUID, uuid4

import pytz
from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db import entities
from db.connection import get_db
from exceptions import PromoNotFoundException, NoAvailableActivationsException, PromoIsNotStartedException, \
    PromoIsExpiredException, PromoIsNotConnectedWithUser, PromoIsNotActiveException, PromoIsNotConnectedWithService
from models import Promo, DiscountType, PromoInfo, Product


class PromoService:
    def __init__(self, postgres_db: AsyncSession):
        self._db: AsyncSession = postgres_db

    async def get_by_code(self, code: str) -> Promo | None:
        result = await self._db.execute(
            select(entities.Promo).options(selectinload(entities.Promo.products)).where(entities.Promo.code == code)
        )
        promo = result.scalars().first()
        if promo is None:
            return None

        return Promo(
            id=promo.id,
            title=promo.title,
            description=promo.description,
            code=promo.code,
            start_at=promo.start_at,
            expired=promo.expired,
            user_id=promo.user_id,
            all_activations_count=promo.activates_possible,
            left_activations_count=promo.activates_left,
            discount_type=DiscountType(promo.discount_type),
            discount_amount=promo.discount_amount,
            service_ids=[product.id for product in promo.products]
        )

    async def get_by_user_id(self, user_id: UUID) -> list[Promo]:
        result = await self._db.execute(
            select(entities.Promo)
            .options(selectinload(entities.Promo.products))
            .where(entities.Promo.user_id == user_id)
        )
        promos = result.scalars().all()

        return [
            Promo(
                id=promo.id,
                title=promo.title,
                description=promo.description,
                code=promo.code,
                start_at=promo.start_at,
                expired=promo.expired,
                user_id=promo.user_id,
                all_activations_count=promo.activates_possible,
                left_activations_count=promo.activates_left,
                discount_type=DiscountType(promo.discount_type),
                discount_amount=promo.discount_amount,
                service_ids=[product.id for product in promo.products]
            )
            for promo in promos
        ]

    async def activate(self, code: str, user_id: UUID, service_id: UUID) -> PromoInfo:
        result = await self._db.execute(
            select(entities.Promo).options(selectinload(entities.Promo.products)).where(entities.Promo.code == code)
        )
        promo = result.scalars().first()
        if promo is None:
            raise PromoNotFoundException(code)
        await self._check_promo(promo, user_id, service_id)
        await self._activate_promo(promo, user_id)
        return PromoInfo(
            discount_type=DiscountType(promo.discount_type),
            discount_amount=promo.discount_amount,
        )

    async def _check_promo(self, promo: entities.Promo, user_id: UUID, service_id: UUID) -> None:
        if not promo.is_active:
            raise PromoIsNotActiveException(promo.code)

        if (promo.user_id is not None) and (promo.user_id != user_id):
            raise PromoIsNotConnectedWithUser(promo.code, user_id)

        service_ids = [product.id for product in promo.products]
        if (len(service_ids) > 0) and (service_id not in service_ids):
            raise PromoIsNotConnectedWithService(promo.code, service_id)

        if promo.activates_left <= 0:
            raise NoAvailableActivationsException(promo.code)

        if promo.start_at > datetime.now(pytz.UTC):
            raise PromoIsNotStartedException(promo.code)

        if promo.expired <= datetime.now(pytz.UTC):
            raise PromoIsExpiredException(promo.code)

    async def _activate_promo(self, promo: entities.Promo, user_id: UUID) -> None:
        new_activates_left = promo.activates_left - 1
        await self._db.execute(
            update(entities.Promo).where(entities.Promo.code == promo.code).values(activates_left=new_activates_left)
        )
        await self._db.commit()

        history_record = entities.History(
            id=uuid4(),
            applied_user_id=user_id,
            discount_amount=promo.discount_amount,
            billing_info="активация промокода",
            promocode_id=promo.id,
        )
        self._db.add(history_record)
        await self._db.commit()

    async def deactivate(self, code: str, user_id: UUID) -> None:
        result = await self._db.execute(
            select(entities.Promo).options(selectinload(entities.Promo.products)).where(entities.Promo.code == code)
        )
        promo = result.scalars().first()
        if promo is None:
            raise PromoNotFoundException(code)
        if (promo.user_id is not None) and (promo.user_id != user_id):
            raise PromoIsNotConnectedWithUser(promo.code, user_id)
        await self._deactivate_promo(promo, user_id)

    async def _deactivate_promo(self, promo: entities.Promo, user_id: UUID) -> None:
        if promo.activates_left < promo.activates_possible:
            new_activates_left = promo.activates_left + 1
            await self._db.execute(
                update(entities.Promo)
                .where(entities.Promo.code == promo.code)
                .values({"activates_left": new_activates_left})
            )
            await self._db.commit()

        history_record = entities.History(
            id=uuid4(),
            applied_user_id=user_id,
            discount_amount=promo.discount_amount,
            billing_info="деактивация промокода",
            promocode_id=promo.id,
        )
        self._db.add(history_record)
        self._db.commit()

    async def get_products(self) -> list[Product]:
        result = await self._db.execute(select(entities.Product))
        products = result.scalars().all()
        return [
            Product(
                id=product.id,
                name=product.name,
                description=product.description,
                price=product.price,
            )
            for product in products
        ]


@lru_cache()
def get_promo_service(postgres_db: AsyncSession = Depends(get_db)) -> PromoService:
    return PromoService(postgres_db)
