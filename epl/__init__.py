from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)

# สร้างโฟลเดอร์ instance ถ้ายังไม่มี
instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'instance')
os.makedirs(instance_path, exist_ok=True)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///epl.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'  # จำเป็นสำหรับ flash messages

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# ✅ เปิด import (ลบ comment ออก)
from epl import routes, models