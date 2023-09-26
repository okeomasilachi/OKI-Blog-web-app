from flask import Flask, render_template, url_for
app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True, port=5001)
