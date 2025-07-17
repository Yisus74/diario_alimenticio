#!/usr/bin/env python3
"""
Script de reparación automática para el Diario de Alimentación Consciente
Soluciona problemas comunes automáticamente
"""

import os
import sys
import subprocess
from datetime import datetime

def ejecutar_comando(comando, descripcion):
    """Ejecuta un comando y muestra el resultado"""
    print(f"🔧 {descripcion}...")
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {descripcion} completado")
            return True
        else:
            print(f"❌ Error en {descripcion}: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error ejecutando {descripcion}: {e}")
        return False

def crear_directorios():
    """Crea los directorios necesarios"""
    print("📁 Creando directorios necesarios...")
    
    directorios = ['templates', 'uploads']
    
    for directorio in directorios:
        try:
            os.makedirs(directorio, exist_ok=True)
            print(f"✅ Directorio '{directorio}' listo")
        except Exception as e:
            print(f"❌ Error creando directorio '{directorio}': {e}")

def reinstalar_dependencias():
    """Reinstala todas las dependencias"""
    print("📦 Reinstalando dependencias...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt no encontrado")
        return False
    
    # Desinstalar dependencias existentes
    ejecutar_comando("pip uninstall flask werkzeug reportlab jinja2 -y", 
                    "Desinstalando dependencias existentes")
    
    # Reinstalar dependencias
    return ejecutar_comando("pip install -r requirements.txt", 
                           "Instalando dependencias")

def reparar_base_datos():
    """Repara o recrea la base de datos"""
    print("🗃️ Reparando base de datos...")
    
    # Hacer backup si existe
    if os.path.exists('diario_alimentacion.db'):
        backup_name = f"diario_alimentacion_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
        try:
            import shutil
            shutil.copy2('diario_alimentacion.db', backup_name)
            print(f"✅ Backup creado: {backup_name}")
        except Exception as e:
            print(f"⚠️  No se pudo crear backup: {e}")
    
    # Recrear base de datos
    try:
        if os.path.exists('database.py'):
            resultado = ejecutar_comando("python -c \"from database import init_database; init_database()\"", 
                                        "Recreando base de datos")
            return resultado
        else:
            print("❌ database.py no encontrado")
            return False
    except Exception as e:
        print(f"❌ Error reparando base de datos: {e}")
        return False

def verificar_y_reparar_flask():
    """Verifica y repara problemas específicos de Flask"""
    print("🌶️ Verificando Flask...")
    
    try:
        import flask
        version = flask.__version__
        print(f"✅ Flask {version} detectado")
        
        # Verificar que la versión sea compatible
        version_parts = version.split('.')
        major = int(version_parts[0])
        minor = int(version_parts[1]) if len(version_parts) > 1 else 0
        
        if major < 2:
            print("⚠️  Versión de Flask muy antigua, actualizando...")
            return ejecutar_comando("pip install --upgrade Flask>=2.0.0", 
                                   "Actualizando Flask")
        else:
            print("✅ Versión de Flask compatible")
            return True
            
    except ImportError:
        print("❌ Flask no está instalado")
        return ejecutar_comando("pip install Flask>=2.0.0", 
                               "Instalando Flask")

def limpiar_cache():
    """Limpia los archivos de cache de Python"""
    print("🧹 Limpiando cache de Python...")
    
    import shutil
    
    # Eliminar __pycache__
    for root, dirs, files in os.walk('.'):
        for dir_name in dirs[:]:
            if dir_name == '__pycache__':
                try:
                    shutil.rmtree(os.path.join(root, dir_name))
                    print(f"✅ Eliminado cache: {os.path.join(root, dir_name)}")
                except Exception as e:
                    print(f"⚠️  No se pudo eliminar {dir_name}: {e}")
    
    # Eliminar archivos .pyc
    for root, dirs, files in os.walk('.'):
        for file_name in files:
            if file_name.endswith('.pyc'):
                try:
                    os.remove(os.path.join(root, file_name))
                    print(f"✅ Eliminado: {file_name}")
                except Exception as e:
                    print(f"⚠️  No se pudo eliminar {file_name}: {e}")

def test_aplicacion():
    """Prueba que la aplicación se pueda importar correctamente"""
    print("🧪 Probando la aplicación...")
    
    try:
        # Intentar importar módulos principales
        from database import init_database, DatabaseManager
        print("✅ database.py importado correctamente")
        
        # Intentar importar app (sin ejecutar)
        import importlib.util
        spec = importlib.util.spec_from_file_location("app", "app.py")
        if spec is None:
            print("❌ No se pudo cargar app.py")
            return False
        
        print("✅ app.py se puede cargar")
        return True
        
    except Exception as e:
        print(f"❌ Error probando la aplicación: {e}")
        return False

def menu_reparacion():
    """Muestra el menú de opciones de reparación"""
    print("\n🔧 HERRAMIENTAS DE REPARACIÓN")
    print("=" * 40)
    print("1. Reparación completa (recomendado)")
    print("2. Solo reinstalar dependencias")
    print("3. Solo reparar base de datos")
    print("4. Solo verificar Flask")
    print("5. Solo limpiar cache")
    print("6. Crear directorios faltantes")
    print("7. Ejecutar diagnóstico")
    print("8. Verificación rápida")
    print("0. Salir")
    print("=" * 40)
    
    try:
        opcion = input("Selecciona una opción (0-8): ").strip()
        return opcion
    except KeyboardInterrupt:
        print("\n👋 Operación cancelada")
        return "0"

def reparacion_completa():
    """Ejecuta todas las reparaciones"""
    print("🚀 INICIANDO REPARACIÓN COMPLETA")
    print("=" * 50)
    
    pasos = [
        ("Creando directorios", crear_directorios),
        ("Limpiando cache", limpiar_cache),
        ("Verificando Flask", verificar_y_reparar_flask),
        ("Reinstalando dependencias", reinstalar_dependencias),
        ("Reparando base de datos", reparar_base_datos),
        ("Probando aplicación", test_aplicacion)
    ]
    
    resultados = []
    for descripcion, funcion in pasos:
        print(f"\n📋 {descripcion}...")
        try:
            resultado = funcion()
            resultados.append(resultado)
            if resultado:
                print(f"✅ {descripcion} completado")
            else:
                print(f"❌ {descripcion} falló")
        except Exception as e:
            print(f"❌ Error en {descripcion}: {e}")
            resultados.append(False)
    
    exitos = sum(resultados)
    total = len(resultados)
    
    print(f"\n📊 RESULTADO: {exitos}/{total} pasos completados exitosamente")
    
    if exitos == total:
        print("🎉 ¡Reparación completada exitosamente!")
        print("   Ahora puedes ejecutar: python app.py")
    else:
        print("⚠️  Algunos pasos fallaron. Revisa los errores arriba.")

def main():
    """Función principal"""
    print("🔧 HERRAMIENTA DE REPARACIÓN")
    print("   Diario de Alimentación Consciente")
    print("=" * 50)
    
    while True:
        opcion = menu_reparacion()
        
        if opcion == "0":
            print("👋 ¡Hasta luego!")
            break
        elif opcion == "1":
            reparacion_completa()
        elif opcion == "2":
            reinstalar_dependencias()
        elif opcion == "3":
            reparar_base_datos()
        elif opcion == "4":
            verificar_y_reparar_flask()
        elif opcion == "5":
            limpiar_cache()
        elif opcion == "6":
            crear_directorios()
        elif opcion == "7":
            # Ejecutar diagnóstico
            try:
                import diagnostico
                diagnostico.main()
            except:
                ejecutar_comando("python diagnostico.py", "Ejecutando diagnóstico")
        elif opcion == "8":
            # Verificación rápida
            try:
                import verificar
                verificar.main()
            except:
                ejecutar_comando("python verificar.py", "Ejecutando verificación rápida")
        else:
            print("❌ Opción no válida")
        
        if opcion != "0":
            input("\nPresiona Enter para continuar...")

if __name__ == "__main__":
    main()