from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import db
from dataclasses import dataclass


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
    __tablename__ = "avg_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[int] = mapped_column("date_time", unique=True)
    value: Mapped[int] = mapped_column("moisture_reading")


@dataclass
class MoistureReading(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[int] = mapped_column(unique=True)
    value: Mapped[int]
