from typing import TypeVar

from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData, String, Integer, Boolean
from sqlalchemy import TIMESTAMP
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

M = TypeVar("M")

SCHEMA_NAME = "content"

metadata = MetaData(schema=SCHEMA_NAME)
Base = declarative_base(metadata=metadata)


class BaseTable(Base):
    __abstract__ = True
    __table_args__ = (
        {
            'schema': SCHEMA_NAME
        }
    )


class Promo(BaseTable):
    __tablename__ = "promo"

    id = Column("id", UUID(as_uuid=True), primary_key=True)
    created = Column("created", TIMESTAMP, default=func.now(), nullable=False)
    modified = Column("modified", TIMESTAMP, default=func.now(), nullable=False)

    title = Column("title", String, nullable=False)
    description = Column("description", String, nullable=False)
    code = Column("code", String, nullable=False, index=True)
    start_at = Column("start_at", TIMESTAMP, default=func.now(), nullable=False)
    expired = Column("expired", TIMESTAMP, default=func.now(), nullable=False)
    user_id = Column("user_id", UUID(as_uuid=True))
    activates_possible = Column("activates_possible", Integer, default=0, nullable=False)
    activates_left = Column("activates_left", Integer, default=0, nullable=False)
    discount_type = Column("discount_type", String, nullable=False)
    discount_amount = Column("discount_amount", Float, default=0, nullable=False)
    minimal_amount = Column("minimal_amount", Float, default=0, nullable=False)
    is_active = Column("is_active", Boolean, nullable=False, default=0)


class History(BaseTable):
    __tablename__ = "history"

    id = Column("id", UUID(as_uuid=True), primary_key=True)
    created = Column("created", TIMESTAMP, default=func.now(), nullable=False)
    modified = Column("modified", TIMESTAMP, default=func.now(), nullable=False)

    applied_user_id = Column("applied_user_id", UUID(as_uuid=True))
    discount_amount = Column("discount_amount", Float, default=0, nullable=False)
    billing_info = Column("billing_info", String, nullable=False)

    promocode_id = Column(
        "promocode_id", UUID(as_uuid=True), ForeignKey("promo.id", ondelete="CASCADE"), nullable=False, index=True
    )


