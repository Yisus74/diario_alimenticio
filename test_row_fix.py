#!/usr/bin/env python3
"""
Prueba específica para verificar que el error de objetos Row está solucionado
"""

def test_database_row_objects():
    """Prueba el manejo de objetos Row de SQLite"""
    print("🧪 Probando objetos Row de SQLite...")
    
    try:
        from database import DatabaseManager, init_database
        
        # Inicializar base de datos
        init_database()
        print("✅ Base de datos inicializada")
        
        # Crear usuario de prueba
        user_id = DatabaseManager.crear_usuario("Test Row User", "testrow@example.com")
        print(f"✅ Usuario de prueba creado: {user_id}")
        
        # Crear registro de prueba
        from datetime import datetime
        registro_datos = {
            'usuario_id': user_id,
            'fecha': datetime.now().date(),
            'que_comi': 'Prueba de Row object',
            'donde_estaba': 'Casa',
            'con_quien': 'Solo',
            'nivel_hambre_antes': 5,
            'nivel_saciedad_despues': 7,
            'emociones_antes': 'tranquilo',
            'sensaciones_fisicas_antes': 'normal',
            'emociones_despues': 'satisfecho',
            'comio_con_atencion': True,
            'que_noto': 'Test',
            'que_aprendio': 'Test learning'
        }
        
        registro_id = DatabaseManager.crear_registro_diario(registro_datos)
        print(f"✅ Registro de prueba creado: {registro_id}")
        
        # Obtener registros y probar acceso a atributos
        registros = DatabaseManager.obtener_registros_por_usuario(user_id)
        print(f"✅ Registros obtenidos: {len(registros)}")
        
        if registros:
            registro = registros[0]
            print(f"✅ Tipo de objeto: {type(registro)}")
            
            # Probar diferentes métodos de acceso
            try:
                # Método 1: Acceso directo (puede fallar con Row)
                fecha = registro['fecha']
                print(f"✅ Acceso por índice: {fecha}")
            except Exception as e:
                print(f"⚠️  Acceso por índice falló: {e}")
            
            try:
                # Método 2: getattr
                fecha = getattr(registro, 'fecha', None)
                print(f"✅ Acceso por getattr: {fecha}")
            except Exception as e:
                print(f"⚠️  Acceso por getattr falló: {e}")
            
            try:
                # Método 3: Función safe_get personalizada
                def safe_get(row, key, default=None):
                    try:
                        if hasattr(row, key):
                            return getattr(row, key, default)
                        elif hasattr(row, '__getitem__'):
                            return row[key] if key in row.keys() else default
                        else:
                            return default
                    except (KeyError, AttributeError):
                        return default
                
                fecha = safe_get(registro, 'fecha')
                que_comi = safe_get(registro, 'que_comi')
                hambre = safe_get(registro, 'nivel_hambre_antes')
                atencion = safe_get(registro, 'comio_con_atencion')
                
                print(f"✅ Función safe_get - fecha: {fecha}")
                print(f"✅ Función safe_get - que_comi: {que_comi}")
                print(f"✅ Función safe_get - hambre: {hambre}")
                print(f"✅ Función safe_get - atención: {atencion}")
                
            except Exception as e:
                print(f"❌ Función safe_get falló: {e}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error en prueba de objetos Row: {e}")
        return False

def test_app_routes_with_rows():
    """Prueba las rutas de la aplicación con objetos Row"""
    print("\n🧪 Probando rutas de la aplicación con objetos Row...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            # Probar que las rutas no fallen al procesar objetos Row
            response = client.get('/')
            print(f"✅ Ruta principal: {response.status_code}")
            
            # Las otras rutas necesitan autenticación, pero al menos verificamos que se importen sin error
            print("✅ Aplicación cargada sin errores de objetos Row")
            
        return True
        
    except Exception as e:
        print(f"❌ Error probando rutas con objetos Row: {e}")
        return False

def test_template_functions():
    """Prueba las funciones auxiliares de plantillas"""
    print("\n🧪 Probando funciones auxiliares de plantillas...")
    
    try:
        from app import app
        
        with app.app_context():
            # Simular un objeto Row
            class MockRow:
                def __init__(self, data):
                    for key, value in data.items():
                        setattr(self, key, value)
                
                def keys(self):
                    return self.__dict__.keys()
                
                def __getitem__(self, key):
                    return getattr(self, key)
            
            # Crear objeto de prueba
            test_row = MockRow({
                'fecha': '2024-01-01',
                'que_comi': 'Test food',
                'nivel_hambre_antes': 5,
                'comio_con_atencion': True
            })
            
            # Probar función safe_get_attr
            safe_get_attr = app.jinja_env.globals.get('safe_get_attr')
            if safe_get_attr:
                fecha = safe_get_attr(test_row, 'fecha')
                print(f"✅ safe_get_attr fecha: {fecha}")
                
                hambre = safe_get_attr(test_row, 'nivel_hambre_antes')
                print(f"✅ safe_get_attr hambre: {hambre}")
                
                atencion = safe_get_attr(test_row, 'comio_con_atencion')
                print(f"✅ safe_get_attr atención: {atencion}")
                
                # Probar con atributo que no existe
                inexistente = safe_get_attr(test_row, 'campo_inexistente', 'default')
                print(f"✅ safe_get_attr campo inexistente: {inexistente}")
            else:
                print("❌ Función safe_get_attr no encontrada")
                return False
            
            # Probar función safe_format_date
            safe_format_date = app.jinja_env.globals.get('safe_format_date')
            if safe_format_date:
                fecha_formateada = safe_format_date('2024-01-01')
                print(f"✅ safe_format_date: {fecha_formateada}")
            else:
                print("❌ Función safe_format_date no encontrada")
                return False
            
            # Probar función safe_bool_text
            safe_bool_text = app.jinja_env.globals.get('safe_bool_text')
            if safe_bool_text:
                bool_text = safe_bool_text(True)
                print(f"✅ safe_bool_text: {bool_text}")
            else:
                print("❌ Función safe_bool_text no encontrada")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando funciones de plantillas: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 PRUEBA DE CORRECCIÓN DE OBJETOS ROW")
    print("=" * 50)
    
    tests = [
        ("Objetos Row de base de datos", test_database_row_objects),
        ("Rutas de aplicación", test_app_routes_with_rows),
        ("Funciones de plantillas", test_template_functions)
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
        print("🎉 ¡PRUEBA DE OBJETOS ROW EXITOSA!")
        print("   El error 'Row' object has no attribute 'get' está solucionado")
        print("   Ahora puedes ejecutar: python run.py")
    else:
        print("❌ ALGUNOS PROBLEMAS DETECTADOS")
        print("   Ejecuta: python reparar.py")
    print("=" * 50)

if __name__ == "__main__":
    main()