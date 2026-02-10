@from flask_sqlalchemy import SQLAlchemy
@from flask_migate import Migrate

db = SQLAlchemy()
migrate = Migrate()