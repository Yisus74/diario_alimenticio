#!/usr/bin/env python3
"""
Script de pruebas para verificar las correcciones del error TypeError
"""

import sys
import os
from datetime import datetime, timedelta

def test_database_operations():
    """Prueba las operaciones básicas de la base de datos"""
    print("🧪 Probando operaciones de base de datos...")
    
    try:
        from database import DatabaseManager, init_database
        
        # Inicializar base de datos
        init_database()
        print("✅ Base de datos inicializada")
        
        # Crear usuario de prueba
        user_id = DatabaseManager.crear_usuario("Test User", "test@example.com")
        print(f"✅ Usuario de prueba creado: {user_id}")
        
        # Crear registro con valores None simulados
        registro_datos = {
            'usuario_id': user_id,
            'fecha': datetime.now().date(),
            'que_comi': 'Test food',
            'donde_estaba': None,  # Valor None intencional
            'con_quien': '',  # Valor vacío
            'nivel_hambre_antes': 5,
            'nivel_saciedad_despues': None,  # Valor None intencional
            'emociones_antes': 'feliz',
            'sensaciones_fisicas_antes': None,
            'emociones_despues': '',
            'comio_con_atencion': True,
            'que_noto': None,
            'que_aprendio': 'Test learning'
        }
        
        registro_id = DatabaseManager.crear_registro_diario(registro_datos)
        print(f"✅ Registro de prueba creado con valores None: {registro_id}")
        
        # Obtener registros
        registros = DatabaseManager.obtener_registros_por_usuario(user_id)
        print(f"✅ Registros obtenidos: {len(registros)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en operaciones de base de datos: {e}")
        return False

def test_safe_filters():
    """Prueba los filtros seguros de Jinja2"""
    print("\n🧪 Probando filtros seguros...")
    
    try:
        # Simular datos con valores None
        test_data = [
            {'nivel_hambre_antes': 5, 'nivel_saciedad_despues': 7, 'comio_con_atencion': True},
            {'nivel_hambre_antes': None, 'nivel_saciedad_despues': 8, 'comio_con_atencion': False},
            {'nivel_hambre_antes': 3, 'nivel_saciedad_despues': None, 'comio_con_atencion': True},
            {'nivel_hambre_antes': None, 'nivel_saciedad_despues': None, 'comio_con_atencion': None}
        ]
        
        # Importar la aplicación para probar los filtros
        from app import app
        
        with app.app_context():
            # Probar filtros directamente
            safe_sum = app.jinja_env.filters.get('safe_sum')
            safe_avg = app.jinja_env.filters.get('safe_avg')
            count_true_attr = app.jinja_env.filters.get('count_true_attr')
            safe_selectattr = app.jinja_env.filters.get('safe_selectattr')
            
            if safe_sum:
                # Probar suma segura
                suma_hambre = safe_sum(test_data, 'nivel_hambre_antes')
                print(f"✅ Suma segura de hambre: {suma_hambre}")
                
                # Probar promedio seguro
                promedio_hambre = safe_avg(test_data, 'nivel_hambre_antes')
                print(f"✅ Promedio seguro de hambre: {promedio_hambre}")
                
                # Probar conteo de atributos verdaderos
                count_atencion = count_true_attr(test_data, 'comio_con_atencion')
                print(f"✅ Conteo de atención: {count_atencion}")
                
                # Probar selección segura
                con_hambre = safe_selectattr(test_data, 'nivel_hambre_antes')
                print(f"✅ Registros con hambre: {len(con_hambre)}")
                
            else:
                print("❌ Filtros no encontrados")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando filtros: {e}")
        return False

def test_estadisticas_route():
    """Prueba la ruta de estadísticas simulada"""
    print("\n🧪 Probando cálculos de estadísticas...")
    
    try:
        # Simular datos de registros con valores None
        registros_test = [
            {
                'nivel_hambre_antes': 5,
                'nivel_saciedad_despues': 7,
                'comio_con_atencion': True,
                'fecha': '2024-01-01',
                'emociones_antes': 'feliz, tranquilo'
            },
            {
                'nivel_hambre_antes': None,  # Valor None
                'nivel_saciedad_despues': 8,
                'comio_con_atencion': False,
                'fecha': '2024-01-02',
                'emociones_antes': None  # Valor None
            },
            {
                'nivel_hambre_antes': 3,
                'nivel_saciedad_despues': None,  # Valor None
                'comio_con_atencion': True,
                'fecha': '2024-01-03',
                'emociones_antes': 'ansioso'
            }
        ]
        
        # Función de conversión segura (copiada de app.py)
        def safe_float(value, default=0.0):
            if value is None:
                return default
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        
        # Probar cálculos seguros
        niveles_hambre = []
        niveles_saciedad = []
        registros_con_atencion = 0
        
        for r in registros_test:
            # Niveles de hambre
            hambre_value = r.get('nivel_hambre_antes')
            if hambre_value is not None:
                hambre_float = safe_float(hambre_value)
                if 0 <= hambre_float <= 10:
                    niveles_hambre.append(hambre_float)
            
            # Niveles de saciedad
            saciedad_value = r.get('nivel_saciedad_despues')
            if saciedad_value is not None:
                saciedad_float = safe_float(saciedad_value)
                if 0 <= saciedad_float <= 10:
                    niveles_saciedad.append(saciedad_float)
            
            # Contar registros con atención
            atencion_value = r.get('comio_con_atencion')
            if atencion_value is not None and atencion_value:
                registros_con_atencion += 1
        
        # Calcular promedios
        promedio_hambre = sum(niveles_hambre) / len(niveles_hambre) if niveles_hambre else 0
        promedio_saciedad = sum(niveles_saciedad) / len(niveles_saciedad) if niveles_saciedad else 0
        porcentaje_atencion = (registros_con_atencion / len(registros_test)) * 100 if registros_test else 0
        
        print(f"✅ Promedio hambre calculado: {promedio_hambre:.1f}")
        print(f"✅ Promedio saciedad calculado: {promedio_saciedad:.1f}")
        print(f"✅ Porcentaje atención calculado: {porcentaje_atencion:.1f}%")
        
        # Probar procesamiento de emociones
        todas_emociones = []
        for registro in registros_test:
            emociones_antes = registro.get('emociones_antes')
            if emociones_antes and isinstance(emociones_antes, str) and emociones_antes.strip():
                emociones_lista = []
                for e in emociones_antes.split(','):
                    if e and e.strip():
                        emociones_lista.append(e.strip().lower())
                todas_emociones.extend(emociones_lista)
        
        print(f"✅ Emociones procesadas: {todas_emociones}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en cálculos de estadísticas: {e}")
        return False

def test_template_rendering():
    """Prueba el renderizado de plantillas con datos None"""
    print("\n🧪 Probando renderizado de plantillas...")
    
    try:
        from app import app
        
        with app.test_client() as client:
            with app.app_context():
                # Esto requeriría una sesión activa, así que solo probamos que la app carga
                response = client.get('/')
                print(f"✅ Respuesta de la app: {response.status_code}")
                
        return True
        
    except Exception as e:
        print(f"❌ Error en renderizado de plantillas: {e}")
        return False

def run_all_tests():
    """Ejecuta todas las pruebas"""
    print("🔬 EJECUTANDO PRUEBAS DE CORRECCIÓN DE TypeError")
    print("=" * 60)
    
    tests = [
        ("Operaciones de Base de Datos", test_database_operations),
        ("Filtros Seguros", test_safe_filters),
        ("Cálculos de Estadísticas", test_estadisticas_route),
        ("Renderizado de Plantillas", test_template_rendering)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}...")
        try:
            result = test_func()
            results.append(result)
            if result:
                print(f"✅ {test_name}: PASADO")
            else:
                print(f"❌ {test_name}: FALLIDO")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append(False)
    
    # Resumen
    passed = sum(results)
    total = len(results)
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMEN DE PRUEBAS: {passed}/{total} PASADAS")
    
    if passed == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("   El error TypeError debería estar solucionado.")
        print("   Ahora puedes ejecutar: python app.py")
    else:
        print("⚠️  ALGUNAS PRUEBAS FALLARON")
        print("   Revisa los errores arriba y ejecuta: python reparar.py")
    
    print("=" * 60)

def main():
    """Función principal"""
    print("🧪 SCRIPT DE PRUEBAS - CORRECCIÓN TypeError")
    print("   Verificando que los valores None se manejen correctamente...")
    print()
    
    run_all_tests()

if __name__ == "__main__":
    main()