import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-temporal-compleja-y-segura'
    