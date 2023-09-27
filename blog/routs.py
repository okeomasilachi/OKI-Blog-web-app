from flask import render_template, url_for, flash, redirect
from blog import app, db, bc
from blog.form import Regfrom, Loginfrom
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

post = [
    {
        "author": "okeoma",
        "title": "my post",
        "content": "my first post",
        "date": "April 21, 2023"
    },
    {
        "author": "onyedibia",
        "title": "next post",
        "content": "another user's post",
        "date": "november 09, 2019"
    }
]


@app.route("/")
@app.route("/home")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template("home.html", posts=post)


@app.route("/About")
@app.route("/about")
def about():
    if not current_user.is_authenticated:
        return redirect(url_for("login"))
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = Regfrom()
    if form.validate_on_submit():
        hp = bc.generate_password_hash(form.password.data).decode("utf-8")
        user = User(uname=form.uname.data, email=form.email.data, password=hp)
        db.session.add(user)
        db.session.commit()
        flash(f"Account Created!", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = Loginfrom()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bc.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f"Welcome Back {user.uname}", "success")
            return redirect(url_for("home"))
        else:
            flash("Login Unsuccessful, Please check Credentials", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout",)
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/account",)
@login_required
def account():
    return render_template("account.html", title="Account")
