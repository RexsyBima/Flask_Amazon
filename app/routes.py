from flask import request
from app import app, catalog
from app.models import SQLProducts
from app.functions import Items, Item, rating_star, get_pagination


@app.route("/")  # ROUTE
def homepage():
    return catalog.render("Home", title="Homepage")


@app.route("/products")  # WIP
def show_products():
    p = request.args.get("page")  # p = page (halaman)
    pagination = get_pagination(page=int(p) if p is not None else 1)
    print(pagination)
    items = Items(
        SQLProducts.query.paginate(page=int(p) if p is not None else 1, per_page=10)
    )
    # if p is not None:
    #    items = Items(SQLProducts.query.paginate(page=int(p), per_page=10))
    # else:
    #    items = Items(SQLProducts.query.paginate(page=1, per_page=10))
    return catalog.render(
        "DisplayProducts",
        title="Show Products",
        items=items,
        pagination=pagination,
        p=int(p),
    )


# @app.route("/item-<id>-<title>")
@app.route("/item")
def show_item():
    id = request.args.get("id")
    if id is not None:
        # title = request.args.get("title")
        item = Item(SQLProducts.query.filter_by(id=id).first())
        item.rating = rating_star(item.rating)
        print(item.rating)
        return catalog.render("DisplayItem", title=item.title, item=item)
    else:
        return {"item": "item not found"}


@app.route("/about")  # WIP
def about_page():
    return "this is about page"


@app.route("/dev/login")
def login():
    return "this is login page"


@app.route("/dev/signup")
def signup():
    return "this is sign up page"
