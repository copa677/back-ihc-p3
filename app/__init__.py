from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config.config import Config
from datetime import timedelta

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Configuraciones específicas de JWT
    app.config['JWT_SECRET_KEY'] = app.config.get('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)




    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.usuarios import usuarios_bp
    from app.routes.datos_envio import datos_envio_bp
    from app.routes.datos_pago import datos_pago_bp
    from app.routes.productos import productos_bp
    from app.routes.orden import orden_bp
    from app.routes.factura import factura_bp
    from app.routes.user_telegram import user_telegram_bp
    from app.routes.delivery import delivery_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(datos_envio_bp, url_prefix='/api/datos-envio')
    app.register_blueprint(datos_pago_bp, url_prefix='/api/datos-pago')
    app.register_blueprint(productos_bp, url_prefix='/api/productos')
    app.register_blueprint(orden_bp, url_prefix='/api/orden')
    app.register_blueprint(factura_bp, url_prefix='/api/factura')
    app.register_blueprint(user_telegram_bp, url_prefix='/api/user-telegram')
    app.register_blueprint(delivery_bp, url_prefix='/api/delivery_bp')

    
    return app