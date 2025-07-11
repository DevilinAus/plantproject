from sqlalchemy.orm import Mapped, mapped_column
from dataclasses import dataclass
from typing import Optional
from sqlalchemy.orm import declarative_base

Base = declarative_base()


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
    value: Mapped[Optional[int]] = mapped_column()


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


@dataclass
class Weather(Base):
    __tablename__ = "weather_current"
    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(unique=True)
    value: Mapped[Optional[str]] = mapped_column()
