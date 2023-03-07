from datetime import datetime
from enum import Enum
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class DiscountType(str, Enum):
    PRICE_FIX = "PRICE_FIX"
    DISCOUNT_PERCENT = "DISCOUNT_PERCENT"
    DISCOUNT_FIX = "DISCOUNT_FIX"


class Promo(BaseOrjsonModel):
    id: UUID
    title: str
    description: str
    code: str
    start_at: datetime
    expired: datetime
    user_id: UUID
    all_activations_count: int
    left_activations_count: int
    discount_type: DiscountType
    discount_amount: float
    service_ids: list[UUID]


class PromoInfo(BaseOrjsonModel):
    discount_type: DiscountType
    discount_amount: float


class ActivationResult(BaseOrjsonModel):
    result: bool
    discount_type: DiscountType | None
    discount_amount: float | None
    error_message: str | None = None


class DeactivationResult(BaseOrjsonModel):
    result: bool
    error_message: str | None = None
