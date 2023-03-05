from datetime import datetime
from functools import lru_cache
from uuid import UUID, uuid4

import pytz
from fastapi import Depends
from sqlalchemy.orm import Session

from db import entities
from db.connection import get_db
from exceptions import PromoNotFoundException, NoAvailableActivationsException, PromoIsNotStartedException, \
    PromoIsExpiredException
from models import Promo, DiscountType


class PromoService:
    def __init__(self, postgres_db: Session):
        self._db: Session = postgres_db

    async def get_by_code(self, code: str) -> Promo | None:
        promo = self._db.query(entities.Promo).filter(entities.Promo.code == code).first()
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
        )


    async def get_by_user_id(self, user_id: UUID) -> list[Promo]:
        promos = self._db.query(entities.Promo).filter(entities.Promo.user_id == user_id).all()
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
            )
            for promo in promos
        ]


    async def activate(self, code: str) -> None:
        promo = self._db.query(entities.Promo).filter(entities.Promo.code == code).first()
        if promo is None:
            raise PromoNotFoundException(code)
        if promo.activates_left <= 0:
            raise NoAvailableActivationsException(code)
        if promo.start_at > datetime.now(pytz.UTC):
            raise PromoIsNotStartedException(code)
        if promo.expired <= datetime.now(pytz.UTC):
            raise PromoIsExpiredException(code)

        new_activates_left = promo.activates_left - 1
        self._db.query(entities.Promo).filter(entities.Promo.code == code).update(
            {"activates_left": new_activates_left}
        )
        history_record = entities.History(
            id=uuid4(),
            applied_user_id=promo.user_id,
            discount_amount=promo.discount_amount,
            billing_info="активация промокода",
            promocode_id=promo.id,
        )
        self._db.add(history_record)
        self._db.commit()


    async def deactivate(self, code: str) -> None:
        promo = self._db.query(entities.Promo).filter(entities.Promo.code == code).first()
        if promo is None:
            raise PromoNotFoundException(code)

        if promo.activates_left < promo.activates_possible:
            new_activates_left = promo.activates_left + 1
            self._db.query(entities.Promo).filter(entities.Promo.code == code).update(
                {"activates_left": new_activates_left}
            )
        history_record = entities.History(
            id=uuid4(),
            applied_user_id=promo.user_id,
            discount_amount=promo.discount_amount,
            billing_info="деактивация промокода",
            promocode_id=promo.id,
        )
        self._db.add(history_record)
        self._db.commit()


@lru_cache()
def get_promo_service(postgres_db: Session = Depends(get_db)) -> PromoService:
    return PromoService(postgres_db)
