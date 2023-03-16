import enum
import json
import logging
import os
from datetime import date
from datetime import datetime
from decimal import Decimal
from typing import Any
from typing import Optional
from uuid import UUID

import sqlalchemy.engine
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

__all__ = ["ConnectionDriver", "ConnectionPool", "create_connection_driver", "get_db"]

from sqlalchemy.orm import sessionmaker, Session
from typing import Dict

logger = logging.getLogger(__name__)


class JsonEncoder(json.JSONEncoder):
    def default(self, value: Any):
        if isinstance(value, (date, datetime)):
            return value.strftime("%Y-%m-%dT%H:%M:%SZ")
        elif isinstance(value, enum.Enum):
            return value.value
        elif isinstance(value, UUID):
            return str(value)
        elif isinstance(value, Decimal):
            return str(value)

        return json.JSONEncoder.default(self, value)


def json_serializer(value: Any):
    return json.dumps(value, cls=JsonEncoder, ensure_ascii=False)


class ConnectionDriver:
    def __init__(self, engine: sqlalchemy.engine.Engine):
        self._engine = engine

    def connect(self) -> sqlalchemy.engine.Connection:
        return self._engine.connect()


def create_connection_driver(database_url: str, application_name: Optional[str] = None) -> ConnectionDriver:
    if not isinstance(database_url, str):
        raise ValueError("Unable to create database driver, database_url must be str")
    connect_args: Dict[str, Any] = {"connect_timeout": 2}
    if application_name is not None and application_name != "":
        connect_args["application_name"] = application_name
    engine = create_engine(database_url, json_serializer=json_serializer, connect_args=connect_args)
    return ConnectionDriver(engine)


class DatabaseError(Exception):
    pass


class ConnectionPool:
    def __init__(self, connection_driver: ConnectionDriver):
        self._connection_driver = connection_driver

    def open(self) -> sqlalchemy.engine.Connection:
        try:
            return self._connection_driver.connect()
        except OperationalError:
            raise DatabaseError()


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://app:123qwe@postgres:5432/promo_db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
