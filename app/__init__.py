import os
import json
from flask import Flask
from flask_cors import CORS
from firebase_admin import credentials, firestore, initialize_app
from .socket_config import socketio

def create_app():
    app = Flask(__name__)

    CORS(app)
    socketio.init_app(app, cors_allowed_origins="*")
    firebase_credentials_path = os.getenv("FIREBASE_CREDENTIALS")
    if not firebase_credentials_path or not os.path.exists(firebase_credentials_path):
        raise FileNotFoundError("Service account key file not found. Check FIREBASE_CREDENTIALS environment variable.")

    with open(firebase_credentials_path, 'r') as f:
        cred_dict = json.load(f)

    cred = credentials.Certificate(cred_dict)
    initialize_app(cred)
    app.db = firestore.client()

    from .routes.user_routes import user_bp
    from .routes.user_transaction_routes import transaction_bp
    from .routes.config_routes import config_bp
    from .routes.user_wallet_routes import wallet_bp

    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(wallet_bp, url_prefix='/api')
    app.register_blueprint(transaction_bp, url_prefix='/api')
    app.register_blueprint(config_bp, url_prefix='/api')

    return app