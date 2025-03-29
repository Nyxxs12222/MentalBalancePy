from flask import Flask
from flask_mysqldb import MySQL
import os

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    
    app.config.from_pyfile(os.path.join(os.path.dirname(__file__), '../config.py'))
    
    # Configuración manual para MySQL (por si acaso)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '79octubre'
    app.config['MYSQL_DB'] = 'MentalBalance'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    
    # Inicializar MySQL
    mysql.init_app(app)
    
    register_blueprints(app)
    
    return app

def register_blueprints(app):
    from app.routes.general import general_bp
    from app.routes.auth import auth_bp
    
    app.register_blueprint(general_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')