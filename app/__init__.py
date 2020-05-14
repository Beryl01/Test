import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate, MigrateCommand
from flask_uploads import UploadSet,configure_uploads,IMAGES

app = Flask(__name__)
app.config['SECRET_KEY'] = '04b4d09c2654641ff1c532479476d7d8'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
configure_uploads(app,photos)
UPLOADED_PHOTOS_DEST ='app/static/images'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
migrate = Migrate(app,db)
mail = Mail(app)

from app import routes