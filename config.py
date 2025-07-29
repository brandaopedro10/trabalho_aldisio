import os
from datetime import timedelta

class Config:
    SECRET_KEY = 'VcKzHS4g2h+dP33tCbqOghtKaU37wvFECMhVqrfccaoI/17qh/j3+VDV'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///usuarios.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'minha_chave_jwt'

    # Token expira em X minutos
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=1)

    UPLOAD_FOLDER = 'static/imagens'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}