from datetime import datetime, timedelta
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from config.config import settings

CREATED_BY = settings.CREATED_BY


class DType(str, Enum):
    PRICE_FIX = 'fixed_price'
    DISCOUNT_PERCENT = 'percentage_discount'
    DISCOUNT_FIX = 'fixed_discount'


class DataParam(BaseModel):
    title: str
    description: str
    start_at: datetime = datetime.now()
    expired: datetime = datetime.now() + timedelta(days=10000),
    activates_possible: int
    discount_type: DType
    discount_amount: int
    minimal_amount: int
    product_id: list[UUID] | None
    created_by = CREATED_BY
    is_active: bool = True
    path: str
    count_codes: int
