from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_modus import Modus
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user
import os
from project.users.forms import LoginForm



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'postgres://localhost/warbler-db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or "it's a secret"

modus = Modus(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.messages.views import messages_blueprint
from project.users.models import User
from project.messages.models import Message
from project.users.models import FollowersFollowee



app.register_blueprint(users_blueprint, url_prefix='/users')
app.register_blueprint(messages_blueprint, url_prefix='/users/<int:id>/messages')

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def root():
    form =LoginForm()
    if current_user.is_anonymous != True:
        messages = Message.query.join(FollowersFollowee, Message.user_id== FollowersFollowee.c.follower_id).filter(FollowersFollowee.c.followee_id==current_user.id).limit(100).all()
        return render_template('home.html', messages=messages)
    else:
        messages = Message.query.order_by("timestamp asc").limit(100).all()
    return render_template('home.html', messages=messages)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
