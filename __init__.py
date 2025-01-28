import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf.csrf import CSRFProtect
from .models import db, User
from .routes.User import user_bp
from flask_login import LoginManager, current_user, login_required
from .models.User import Users
from datetime import datetime, timedelta
from flask_socketio import SocketIO
from flask_migrate import Migrate

app = Flask(__name__, static_folder='static', static_url_path='/static')
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'site.db')
app.config['SECRET_KEY'] = 'FBJOHFBFHJbewjfnkBFJEwkpnfkwafnjweotfjpwjrfr83rfhJNJFbej'  # Replace with a random string!
csrf = CSRFProtect(app)
csrf.init_app(app)

app.register_blueprint(user_bp, url_prefix='/user')

login_manager = LoginManager(app)
login_manager.login_view = 'user.login'
login_manager.login_message = 'Вы не можете получить доступ к этой странице, авторизуйтесь'
login_manager.login_message_category = 'info' 
socketio = SocketIO(app)


login_manager.init_app(app) 
db.init_app(app)
migrate = Migrate(app, db) # app - ваш объект Flask приложения, db - ваш объект SQLAlchemy

@login_manager.user_loader
def load_user(user_id):
    try:
        print( Users.query.get(int(user_id)))
        return Users.query.get(int(user_id))
    except Exception as e:
        print(e)


with app.app_context():
    db.create_all()




@app.route("/index")
@app.route("/")
def index():
    return render_template("templates/index.html", show_header=True, show_footer=True)


