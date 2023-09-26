from flask import Flask, render_template, url_for
from form import Regfrom, Loginfrom

app = Flask(__name__)

app.config["SECRET_KEY"] = 'a6a5a924edbe24ccb72f3384a684a69ed6f4b3f43f00d6eca8cb735abc5214e80cd559f4723397dbb1e4b73d926c15052738'

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
    return render_template("home.html", posts=post)


@app.route("/About")
@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register")
def register():
    form = Regfrom()
    return render_template("register.html", title="Register", form=form)

@app.route("/login")
def login():
    form = Loginfrom()
    return render_template("login.html", title="Login", form=form)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
