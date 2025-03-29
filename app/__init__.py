from flask import Flask

def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'clave-temporal' 
    
    # Solo registramos el blueprint general
    from app.routes.general import general_bp
    app.register_blueprint(general_bp)
    
    return app