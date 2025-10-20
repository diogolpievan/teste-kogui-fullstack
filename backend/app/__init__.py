from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
from extensions import db, bcrypt, jwt
import os


def create_app():
    app = Flask(__name__)
    
    load_dotenv()
    
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 86400 
    
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    CORS(app)
    
    from app.routes.auth import auth_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/usuarios')
    
    with app.app_context():
        db.create_all()
    
    return app
