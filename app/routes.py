from flask import redirect, request, url_for
from flask_login import login_user, current_user
from app import app, catalog, db, bcrypt, login_manager
from app.models import Comments, SQLProducts, Users
from app.functions import Items, Item, rating_star, get_pagination
from app.forms import CommentForm, LoginForm, RegisterForm


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(id=user_id).first()


@app.route("/")  # ROUTE
@app.route("/home")
def homepage():
    print(current_user.is_authenticated)
    print(current_user.email, current_user.username)
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
@app.route("/item", methods=["GET", "POST"])
def show_item():
    id = request.args.get("id")
    form = CommentForm()
    if id is not None:
        if form.validate_on_submit():
            comment = Comments()
            comment.username = current_user.username
            comment.comment = form.comment
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for("show_item", id=id))
        item = Item(SQLProducts.query.filter_by(id=id).first())
        item.rating = rating_star(item.rating)
        print(item.rating)
        return catalog.render("DisplayItem", title=item.title, item=item, form=form)
    else:
        return {"item": "item not found"}


@app.route("/about")  # WIP
def about_page():
    return "this is about page"


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user: Users = Users.query.filter_by(email=form.email.data).first()
        check_pass = bcrypt.check_password_hash(user.password, form.password.data)
        if check_pass:
            print("successful login")
            login_user(user)

        """
        1. jika email ada di database, maka ambil user itu
        2. jika input password == password di database -> login
        2a. gunakan fitur bcrypt untuk ngecek validasi password poin 2
        """
        return redirect(url_for("login"))
    return catalog.render("Login", title="Login Page", form=form)


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
