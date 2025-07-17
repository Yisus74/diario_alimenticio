"""
Configuración de la aplicación Diario de Alimentación Consciente
"""
import os
from datetime import timedelta

class Config:
    """Configuración base"""
    
    # Clave secreta para sesiones (cambiar en producción)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'tu_clave_secreta_muy_segura_aqui'
    
    # Base de datos
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'diario_alimentacion.db'
    
    # Configuraciones de sesión
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Cambiar a True en producción con HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Directorio de uploads
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Configuración de la aplicación
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 5000

class DevelopmentConfig(Config):
    """Configuración para desarrollo"""
    DEBUG = True
    
class ProductionConfig(Config):
    """Configuración para producción"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY debe estar definida en producción")

class TestingConfig(Config):
    """Configuración para testing"""
    TESTING = True
    DATABASE_PATH = ':memory:'  # Base de datos en memoria para tests

# Diccionario de configuraciones disponibles
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Obtiene la configuración basada en la variable de entorno"""
    return config[os.environ.get('FLASK_ENV', 'default')]