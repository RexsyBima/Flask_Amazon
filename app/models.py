from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel
from app import db
from app import app


class SQLProducts(db.Model):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    url = Column(String)
    title = Column(String)
    price = Column(Float)
    total_rating = Column(Integer)
    rating = Column(Float)
    brand = Column(String)
    img_url = Column(String)


class Users(db.Model):
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


with app.app_context():
    db.create_all()


class PYProducts(BaseModel):
    id: int
    url: str
    title: str
    price: float
    total_rating: int
    rating: float | list
    brand: str
    img_url: str
