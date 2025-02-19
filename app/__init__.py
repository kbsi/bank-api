import logging
from flask import Flask
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_cors import CORS
from dotenv import load_dotenv
import os
from app.services.mongo import init_app as init_mongo
from app.services.mongo_handler import MongoHandler

load_dotenv()  # Charger les variables d'environnement

jwt = JWTManager()


def create_app():
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    # Set pymongo logging level to WARNING to reduce verbosity
    logging.getLogger("pymongo").setLevel(logging.WARNING)

    logger.debug("Début de la création de l'application Flask...")

    app = Flask(__name__)
    # Charger la configuration depuis config.py
    app.config.from_object('app.config.Config')

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

    logger.debug("Configuration de l'application Flask chargée.")

    logger.debug("Initialisation de PyMongo...")
    try:
        init_mongo(app)
        logger.debug("PyMongo initialisé avec succès.")
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de PyMongo: {e}")

    # Add MongoDB log handler
    mongo_handler = MongoHandler()
    mongo_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    mongo_handler.setFormatter(formatter)
    logger.addHandler(mongo_handler)

    jwt.init_app(app)

    swagger = Swagger(app, template={
        "swagger": "2.0",
        "info": {
            "title": "Bank API",
            "description": "API pour la gestion des comptes bancaires",
            "version": "1.0.0"
        },
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
            }
        },
        "security": [
            {
                "Bearer": []
            }
        ]
    })

    from app.routes.auth import auth_bp
    from app.routes.accounts import accounts_bp
    from app.routes.admin import admin_bp
    from app.routes.logs import logs_bp  # Importer le blueprint des logs

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(accounts_bp, url_prefix="/api/accounts")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    # Enregistrer le blueprint des logs
    app.register_blueprint(logs_bp, url_prefix="/api")

    logger.debug("Fin de la création de l'application Flask.")

    return app
