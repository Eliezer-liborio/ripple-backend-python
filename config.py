import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Configurações base"""
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:senha@localhost:5432/ripple_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    
    # JWT
    JWT_SECRET = os.getenv('JWT_SECRET', 'jwt-secret-key')
    JWT_REFRESH_SECRET = os.getenv('JWT_REFRESH_SECRET', 'jwt-refresh-secret-key')
    JWT_EXPIRES_IN = int(os.getenv('JWT_EXPIRES_IN', 900))  # 15 minutos
    JWT_REFRESH_EXPIRES_IN = int(os.getenv('JWT_REFRESH_EXPIRES_IN', 604800))  # 7 dias
    
    # CORS
    CORS_ORIGIN = os.getenv('CORS_ORIGIN', 'http://localhost:3000,http://localhost:5173').split(',')
    
    # Server
    PORT = int(os.getenv('PORT', 5000))
    HOST = os.getenv('HOST', '0.0.0.0')

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
