from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_migrate import Migrate



app = Flask(__name__)

# สร้างโฟลเดอร์ instance ถ้ายังไม่มี
instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
os.makedirs(instance_path, exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///epl.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate = Migrate(app, db)


db = SQLAlchemy(app)

from epl import routes, models