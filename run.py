#!/usr/bin/env python3
"""
Script de ejecución para el Diario de Alimentación Consciente
Maneja la inicialización y arranque de la aplicación
"""

import os
import sys

def verificar_dependencias():
    """Verifica que Flask esté instalado"""
    try:
        import flask
        print(f"✅ Flask {flask.__version__} detectado")
        return True
    except ImportError:
        print("❌ Flask no está instalado")
        print("Ejecuta: pip install -r requirements.txt")
        return False

def main():
    """Función principal"""
    print("🌱 DIARIO DE ALIMENTACIÓN CONSCIENTE")
    print("=" * 50)
    
    # Verificar dependencias
    if not verificar_dependencias():
        sys.exit(1)
    
    # Verificar que los archivos existan
    archivos_necesarios = ['app.py', 'database.py']
    for archivo in archivos_necesarios:
        if not os.path.exists(archivo):
            print(f"❌ Archivo {archivo} no encontrado")
            sys.exit(1)
    
    print("🚀 Iniciando aplicación...")
    
    # Importar y ejecutar la aplicación
    try:
        from app import app
        
        # Crear directorio uploads si no existe
        os.makedirs('uploads', exist_ok=True)
        
        print("📱 Aplicación disponible en: http://localhost:5000")
        print("🛑 Presiona Ctrl+C para detener")
        print("=" * 50)
        
        app.run(debug=True, host='127.0.0.1', port=5000)
        
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario")
    except Exception as e:
        print(f"❌ Error al ejecutar la aplicación: {e}")
        print("\nSoluciones posibles:")
        print("1. Verifica que todas las dependencias estén instaladas")
        print("2. Ejecuta: python init.py")
        print("3. Verifica que el puerto 5000 no esté en uso")

if __name__ == "__main__":
    main()