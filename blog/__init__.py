from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)

app.config["SECRET_KEY"] = 'a6a5a924edbe24ccb72f3384a684a69ed6f4b3f43f00d6eca8cb735abc5214e80cd559f4723397dbb1e4b73d926c15052738'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"

db = SQLAlchemy(app)
bc = Bcrypt(app)
login = LoginManager(app)
login.login_view = "login"
login.login_message_category = "info"


from blog import routs
