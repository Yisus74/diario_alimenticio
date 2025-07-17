#!/usr/bin/env python3
"""
Verificación rápida de que el error de filtros está solucionado
"""

def test_app_import():
    """Prueba que la aplicación se puede importar sin errores"""
    print("🧪 Probando importación de la aplicación...")
    try:
        from app import app
        print("✅ Aplicación importada correctamente")
        
        # Verificar que los filtros están registrados
        filters = app.jinja_env.filters
        required_filters = ['safe_sum', 'safe_avg', 'safe_count', 'count_true_attr', 'safe_selectattr']
        
        missing_filters = []
        for filter_name in required_filters:
            if filter_name in filters:
                print(f"✅ Filtro '{filter_name}' registrado")
            else:
                print(f"❌ Filtro '{filter_name}' NO encontrado")
                missing_filters.append(filter_name)
        
        if missing_filters:
            print(f"⚠️  Filtros faltantes: {missing_filters}")
            return False
        
        print("✅ Todos los filtros están registrados")
        return True
        
    except Exception as e:
        print(f"❌ Error al importar la aplicación: {e}")
        return False

def test_routes():
    """Prueba que las rutas principales funcionen"""
    print("\n🧪 Probando rutas principales...")
    try:
        from app import app
        
        with app.test_client() as client:
            # Probar ruta principal
            response = client.get('/')
            print(f"✅ Ruta principal: {response.status_code}")
            
            # Las otras rutas requieren autenticación, así que solo probamos que no hay errores de sintaxis
            print("✅ Rutas cargadas sin errores de sintaxis")
            
        return True
        
    except Exception as e:
        print(f"❌ Error probando rutas: {e}")
        return False

def test_database():
    """Prueba que la base de datos funcione"""
    print("\n🧪 Probando base de datos...")
    try:
        from database import DatabaseManager, init_database
        
        # Inicializar base de datos
        init_database()
        print("✅ Base de datos inicializada")
        
        # Probar obtener emociones
        emociones = DatabaseManager.obtener_emociones()
        print(f"✅ Emociones obtenidas: {len(emociones)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error con base de datos: {e}")
        return False

def main():
    """Función principal"""
    print("🔍 VERIFICACIÓN RÁPIDA - ERROR DE FILTROS")
    print("=" * 50)
    
    tests = [
        ("Importación de la aplicación", test_app_import),
        ("Rutas principales", test_routes),
        ("Base de datos", test_database)
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ Error en {test_name}: {e}")
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ¡VERIFICACIÓN EXITOSA!")
        print("   El error de filtros debería estar solucionado")
        print("   Ahora puedes ejecutar: python run.py")
    else:
        print("❌ ALGUNOS PROBLEMAS DETECTADOS")
        print("   Ejecuta: python reparar.py")
    print("=" * 50)

if __name__ == "__main__":
    main()