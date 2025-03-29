from flask import Flask
#from flask_login import LoginManager  # Para cuando implementes autenticación

def create_app():
    app = Flask(__name__)
    
    app.config.from_pyfile('../config.py')
    
    #login_manager = LoginManager()
    #login_manager.init_app(app)
    #login_manager.login_view = 'auth.login'  
    
    register_blueprints(app)
    
    return app

def register_blueprints(app):
    from app.routes.general import general_bp
    from app.routes.auth import auth_bp
    #from app.routes.client import client_bp
    #from app.routes.specialist import specialist_bp
    
    app.register_blueprint(general_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    #app.register_blueprint(client_bp, url_prefix='/client')
    #app.register_blueprint(specialist_bp, url_prefix='/specialist')