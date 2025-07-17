#!/usr/bin/env python3
"""
Script de diagnóstico para el Diario de Alimentación Consciente
Verifica la configuración y identifica problemas comunes
"""

import os
import sys
import sqlite3
from datetime import datetime

def verificar_archivos():
    """Verifica que todos los archivos necesarios existan"""
    print("🔍 Verificando archivos del proyecto...")
    
    archivos_necesarios = [
        'app.py',
        'database.py',
        'requirements.txt',
        'templates/base.html',
        'templates/dashboard.html',
        'templates/estadisticas.html'
    ]
    
    archivos_faltantes = []
    for archivo in archivos_necesarios:
        if os.path.exists(archivo):
            print(f"✅ {archivo}")
        else:
            print(f"❌ {archivo}")
            archivos_faltantes.append(archivo)
    
    return len(archivos_faltantes) == 0

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    print("\n🔍 Verificando dependencias...")
    
    dependencias = {
        'flask': 'Flask',
        'reportlab': 'ReportLab',
        'werkzeug': 'Werkzeug'
    }
    
    dependencias_faltantes = []
    for modulo, nombre in dependencias.items():
        try:
            __import__(modulo)
            # Obtener versión si es posible
            try:
                mod = __import__(modulo)
                version = getattr(mod, '__version__', 'unknown')
                print(f"✅ {nombre} ({version})")
            except:
                print(f"✅ {nombre}")
        except ImportError:
            print(f"❌ {nombre}")
            dependencias_faltantes.append(nombre)
    
    return len(dependencias_faltantes) == 0

def verificar_base_datos():
    """Verifica el estado de la base de datos"""
    print("\n🔍 Verificando base de datos...")
    
    db_path = 'diario_alimentacion.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de datos no encontrada: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = [row[0] for row in cursor.fetchall()]
        
        tablas_esperadas = ['usuarios', 'registros_diarios', 'emociones', 'reflexiones_semanales']
        
        print(f"✅ Base de datos encontrada: {db_path}")
        
        for tabla in tablas_esperadas:
            if tabla in tablas:
                # Contar registros
                cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
                count = cursor.fetchone()[0]
                print(f"✅ Tabla '{tabla}': {count} registros")
            else:
                print(f"❌ Tabla faltante: {tabla}")
        
        # Verificar datos de ejemplo
        cursor.execute("SELECT COUNT(*) FROM usuarios")
        usuarios_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM registros_diarios")
        registros_count = cursor.fetchone()[0]
        
        if usuarios_count == 0:
            print("ℹ️  No hay usuarios registrados")
        
        if registros_count == 0:
            print("ℹ️  No hay registros diarios")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error al verificar la base de datos: {e}")
        return False

def verificar_puerto():
    """Verifica si el puerto 5000 está disponible"""
    print("\n🔍 Verificando puerto 5000...")
    
    import socket
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 5000))
        sock.close()
        
        if result == 0:
            print("⚠️  Puerto 5000 está en uso")
            print("   Sugerencia: Detén otras aplicaciones o usa otro puerto")
            return False
        else:
            print("✅ Puerto 5000 disponible")
            return True
    except Exception as e:
        print(f"⚠️  No se pudo verificar el puerto: {e}")
        return True

def test_imports():
    """Prueba importar los módulos principales"""
    print("\n🔍 Probando importaciones...")
    
    try:
        from database import init_database, DatabaseManager
        print("✅ database.py importado correctamente")
        
        # Probar función básica
        try:
            emociones = DatabaseManager.obtener_emociones()
            print(f"✅ Base de datos funcional: {len(emociones)} emociones disponibles")
        except Exception as e:
            print(f"⚠️  Error al acceder a la base de datos: {e}")
        
    except Exception as e:
        print(f"❌ Error al importar database.py: {e}")
        return False
    
    try:
        from flask import Flask
        print("✅ Flask importado correctamente")
    except Exception as e:
        print(f"❌ Error al importar Flask: {e}")
        return False
    
    return True

def generar_reporte():
    """Genera un reporte de diagnóstico"""
    print("\n" + "="*60)
    print("📋 REPORTE DE DIAGNÓSTICO")
    print("="*60)
    
    archivos_ok = verificar_archivos()
    dependencias_ok = verificar_dependencias()
    db_ok = verificar_base_datos()
    puerto_ok = verificar_puerto()
    imports_ok = test_imports()
    
    print("\n📊 RESUMEN:")
    print(f"Archivos del proyecto: {'✅' if archivos_ok else '❌'}")
    print(f"Dependencias: {'✅' if dependencias_ok else '❌'}")
    print(f"Base de datos: {'✅' if db_ok else '❌'}")
    print(f"Puerto disponible: {'✅' if puerto_ok else '⚠️'}")
    print(f"Importaciones: {'✅' if imports_ok else '❌'}")
    
    estado_general = all([archivos_ok, dependencias_ok, db_ok, imports_ok])
    
    print(f"\n🎯 ESTADO GENERAL: {'✅ TODO CORRECTO' if estado_general else '❌ PROBLEMAS DETECTADOS'}")
    
    if not estado_general:
        print("\n💡 SOLUCIONES SUGERIDAS:")
        if not dependencias_ok:
            print("   • Ejecuta: pip install -r requirements.txt")
        if not db_ok:
            print("   • Ejecuta: python init.py")
        if not archivos_ok:
            print("   • Verifica que todos los archivos estén en el directorio correcto")
        if not imports_ok:
            print("   • Reinstala las dependencias: pip install --force-reinstall -r requirements.txt")
    else:
        print("\n🚀 ¡La aplicación debería funcionar correctamente!")
        print("   Para ejecutar: python app.py")
    
    print("="*60)

def main():
    """Función principal"""
    print("🔧 DIAGNÓSTICO DEL DIARIO DE ALIMENTACIÓN CONSCIENTE")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print(f"Directorio: {os.getcwd()}")
    
    generar_reporte()

if __name__ == "__main__":
    main()