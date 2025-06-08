from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import db
from dataclasses import dataclass
from typing import Optional


@dataclass
class Person(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]


@dataclass
class RawData(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[int] = mapped_column(unique=True)
    value: Mapped[int]


@dataclass
class AvgData(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[int] = mapped_column(unique=True)
    value: Mapped[Optional[int]] = mapped_column()


@dataclass
class MoistureReading(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[int] = mapped_column(unique=True)
    value: Mapped[int]
