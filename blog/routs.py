from flask import render_template, url_for, flash, redirect, request, abort
from blog import app, db, bc
import secrets
import os
from PIL import Image
from blog.form import Regfrom, Loginfrom, UpdateAccountFrom, PostForm
from blog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
@login_required
def home():
    page = request.args.get("page", 1, type=int)
    post = Post.query.paginate(page=page, per_page=5)
    return render_template("home.html", posts=post)


@app.route("/About")
@app.route("/about")
@login_required
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = Regfrom()
    if form.validate_on_submit():
        hp = bc.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hp)
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
            next_page = request.args.get("next")
            flash(f"Welcome Back {user.username}", "success")
            print(next_page)
            return redirect(f"{next_page[1:]}") if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful, Please check Credentials", "danger")
    return render_template("login.html", title="Login", form=form)

@app.route("/logout",)
def logout():
    logout_user()
    return redirect(url_for("home"))


def save_pic(form_pic):
    rand_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_pic.filename)
    new_file_name = rand_hex + f_ext
    path = os.path.join(app.root_path, "static/dpics", new_file_name)
    
    size = (125, 125)
    img = Image.open(form_pic)
    img.thumbnail(size)
    img.save(path)
    
    return new_file_name


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountFrom()
    if form.validate_on_submit():
        old_img = None
        if form.picture.data:
            old_img = current_user.image_file
            pic = save_pic(form.picture.data)
            current_user.image_file = pic
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        if old_img and old_img != "default.jpg":
            path = os.path.join(app.root_path, "static/dpics", old_img)
            if os.path.exists(path):
                os.remove(path)
        flash("Account Info Updated", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="dpics/" + current_user.image_file)
    return render_template("account.html", title="Account",
                           image_file=image_file, form=form)


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Post Created", "success")
        return redirect(url_for("home"))
    return render_template("create_post.html", titel="New Post",
                           form=form, legend="New post")

@app.route("/post/<int:post_id>")
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post Updated", "success")
        return redirect(url_for("post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", titel="Update Post",
                           form=form, legend="Update Post")


@app.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post Deleted", "success")
    return redirect(url_for("home"))

