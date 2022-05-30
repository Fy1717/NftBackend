from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()

def createApp():
    app = Flask(__name__,
            static_url_path = '',
            static_folder = '../static/uploads/')
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://postgres:RuM3XXttmhCZQqpq@localhost:5432/ecommerce"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = "ecommerce-secret"
    app.config['UPLOAD_FOLDER'] = "static/uploads/"

    CORS(app)

    migrate = Migrate(app, db)

    db.init_app(app)

    return app
