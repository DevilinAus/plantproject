from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import db
from dataclasses import dataclass


# class Something(db.Model):
#     id: int = db.Column(db.Integer, primary_key=True)
#     name: str = db.Column(db.String)
#     password = db.Columnn(db.String)
#     # because you don't specify a way this should be returned (eg :str)
#     # it won't be returned in the datacalsse


@dataclass
class Person(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
