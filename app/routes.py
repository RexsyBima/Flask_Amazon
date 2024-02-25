from flask import redirect, request, url_for
from app import app, catalog, db, bcrypt
from app.models import SQLProducts, Users
from app.functions import Items, Item, rating_star, get_pagination
from app.forms import RegisterForm


@app.route("/")  # ROUTE
@app.route("/home")
def homepage():
    return catalog.render("Home", title="Homepage")


@app.route("/products")  # WIP
def show_products():
    p = request.args.get("page")  # p = page (halaman)
    pagination = get_pagination(page=int(p) if p is not None else 1)
    print(pagination)
    items = Items(
        SQLProducts.query.paginate(page=int(p) if p is not None else 1, per_page=20)
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
        p=int(p) if p is not None else 1,
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


@app.route("/login")
def login():
    return "this is login page"


@app.route("/register", methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password1.data != form.password2.data:
            print("pls check ur pass")
            return redirect("/register")
        user = Users()
        user.username = form.username.data
        user.email = form.email.data
        password = form.password1.data
        user.password = bcrypt.generate_password_hash(password).decode("utf-8")
        db.session.add(user)
        db.session.commit()
        return redirect("/home")
    return catalog.render("Register", title="Register Page", form=form)
