from sqlalchemy.orm import Mapped, mapped_column
from dataclasses import dataclass
from typing import Optional
from models import Base


@dataclass
class Person(Base):
    __tablename__ = "person"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]


@dataclass
class RawData(Base):
    __tablename__ = "raw_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[int] = mapped_column(unique=True)
    value: Mapped[int]


@dataclass
class AvgData(Base):
    __tablename__ = "avg_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[int] = mapped_column(unique=True)
    value: Mapped[Optional[int]] = mapped_column()


@dataclass
class MoistureReading(Base):
    __tablename__ = "moisture_reading"
    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp: Mapped[int] = mapped_column(unique=True)
    value: Mapped[int]
