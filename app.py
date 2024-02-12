from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from pydantic import BaseModel
import os.path


DB_NAME = "database.db"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, DB_NAME)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"

db = SQLAlchemy(app)


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


class PYProducts(BaseModel):
    id: int
    url: str
    title: str
    price: float
    total_rating: int
    rating: float
    brand: str
    img_url: str


def Item(sql_query: SQLProducts):
    return PYProducts(
        id=sql_query.id,
        url=sql_query.url,
        title=sql_query.title,
        price=sql_query.price,
        total_rating=sql_query.total_rating,
        rating=sql_query.rating,
        brand=sql_query.brand,
        img_url=sql_query.img_url,
    )


def Items(sql_query: SQLProducts):
    return [
        PYProducts(
            id=item.id,
            url=item.url,
            title=item.title,
            price=item.price,
            total_rating=item.total_rating,
            rating=item.rating,
            brand=item.brand,
            img_url=item.img_url,
        ).model_dump()
        for item in sql_query
    ]


@app.route("/")  # ROUTE
def homepage():
    items = Items(SQLProducts.query.all())
    print(items)
    return {"data": items}


@app.route("/product-<id>")
def show_product(id):
    try:
        item = Item(SQLProducts.query.get(id))
        item.title = item.title.replace("        ", "").replace("       ", "")
        item = item.model_dump()
    except AttributeError:
        item = None
    return {"data": item}


# [1,3,4,5,6][-1] -> PRINT 6 (INDEXING TERAKHIR)


if __name__ == "__main__":
    app.run(debug=True)
