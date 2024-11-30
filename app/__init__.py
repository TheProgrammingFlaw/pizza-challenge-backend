from flask import Flask
from flask_cors import CORS
from firebase_admin import credentials, firestore, initialize_app
from .config import Config
from .socket_config import socketio


def create_app():
    app = Flask(__name__)

    # Allow cors and initialise web sockets
    CORS(app)
    socketio.init_app(app, cors_allowed_origins="*")

    # Initialize Firebase
    app.config.from_object(Config)
    cred = credentials.Certificate(app.config['FIREBASE_CREDENTIALS'])
    initialize_app(cred)
    app.db = firestore.client()

    # Register blueprints
    from .routes.user_routes import user_bp
    from .routes.user_transaction_routes import transaction_bp
    from .routes.config_routes import config_bp
    from .routes.user_wallet_routes import wallet_bp

    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(wallet_bp, url_prefix='/api')
    app.register_blueprint(transaction_bp, url_prefix='/api')
    app.register_blueprint(config_bp, url_prefix='/api')

    return app