#!/usr/bin/env python3
"""
Script de inicialización para el Diario de Alimentación Consciente
Configura la base de datos y crea datos de ejemplo opcionalmente.
"""

import os
import sys
from datetime import datetime, timedelta
from database import init_database, DatabaseManager

def crear_datos_ejemplo():
    """Crea algunos datos de ejemplo para demostrar la aplicación"""
    print("¿Deseas crear datos de ejemplo? (s/n): ", end="")
    respuesta = input().lower().strip()
    
    if respuesta not in ['s', 'si', 'sí', 'yes', 'y']:
        return
    
    print("Creando datos de ejemplo...")
    
    # Crear usuario de ejemplo
    try:
        user_id = DatabaseManager.crear_usuario("Usuario Demo", "demo@ejemplo.com")
        print(f"Usuario demo creado con ID: {user_id}")
        
        # Crear algunos registros de ejemplo
        fecha_hoy = datetime.now().date()
        
        registros_ejemplo = [
            {
                'usuario_id': user_id,
                'fecha': fecha_hoy - timedelta(days=2),
                'que_comi': 'Ensalada mixta con pollo, aguacate y vinagreta de limón. Agua natural.',
                'donde_estaba': 'En casa, en el comedor',
                'con_quien': 'Solo/a',
                'nivel_hambre_antes': 6,
                'nivel_saciedad_despues': 7,
                'emociones_antes': 'calmado, hambriento',
                'sensaciones_fisicas_antes': 'Energía normal, un poco de hambre en el estómago',
                'emociones_despues': 'satisfecho, feliz',
                'comio_con_atencion': True,
                'que_noto': 'Me tomé mi tiempo para saborear cada bocado. La ensalada tenía texturas muy variadas.',
                'que_aprendio': 'Cuando como despacio, me siento más satisfecho con menos cantidad.'
            },
            {
                'usuario_id': user_id,
                'fecha': fecha_hoy - timedelta(days=1),
                'que_comi': 'Sandwich de jamón y queso, papas fritas, refresco.',
                'donde_estaba': 'En la oficina',
                'con_quien': 'Compañeros de trabajo',
                'nivel_hambre_antes': 8,
                'nivel_saciedad_despues': 9,
                'emociones_antes': 'estresado, ansioso',
                'sensaciones_fisicas_antes': 'Mucha hambre, algo de tensión en los hombros',
                'emociones_despues': 'pesado, un poco culpable',
                'comio_con_atencion': False,
                'que_noto': 'Comí muy rápido mientras revisaba emails. No presté atención a los sabores.',
                'que_aprendio': 'Cuando estoy estresado, tendo a comer más rápido y elecciones menos saludables.'
            },
            {
                'usuario_id': user_id,
                'fecha': fecha_hoy,
                'que_comi': 'Avena con frutas (plátano, fresas), nueces y miel. Té verde.',
                'donde_estaba': 'En casa, en la cocina',
                'con_quien': 'Familia',
                'nivel_hambre_antes': 5,
                'nivel_saciedad_despues': 6,
                'emociones_antes': 'tranquilo, esperanzado',
                'sensaciones_fisicas_antes': 'Relajado, hambre ligera',
                'emociones_despues': 'energizado, satisfecho',
                'comio_con_atencion': True,
                'que_noto': 'Disfruté mucho la conversación con mi familia. La avena estaba cremosa y las frutas muy dulces.',
                'que_aprendio': 'Comer en compañía y sin prisas hace que la experiencia sea mucho más placentera.'
            }
        ]
        
        for registro in registros_ejemplo:
            DatabaseManager.crear_registro_diario(registro)
        
        print(f"Se crearon {len(registros_ejemplo)} registros de ejemplo")
        
        # Crear una reflexión semanal de ejemplo
        reflexion_ejemplo = {
            'usuario_id': user_id,
            'semana_inicio': fecha_hoy - timedelta(days=6),
            'semana_fin': fecha_hoy,
            'patrones_observados': 'Noto que cuando estoy estresado en el trabajo, tendo a comer más rápido y elijo alimentos menos nutritivos. En casa, cuando estoy relajado, disfruto más la comida y como más conscientemente.',
            'momentos_sin_hambre': 'Ayer en la tarde comí algunas galletas mientras trabajaba, más por aburrimiento que por hambre real.',
            'comidas_disfrutadas': 'El desayuno de hoy con avena y frutas, y la ensalada de anteayer.',
            'que_tenian_comun': 'Ambas las comí sin prisas, prestando atención a los sabores. También tenían muchos colores y texturas variadas.',
            'que_mejorar': 'Quiero practicar tomarme pausas conscientes antes de comer, especialmente en el trabajo. También intentaré preparar snacks saludables para los momentos de estrés.'
        }
        
        DatabaseManager.crear_reflexion_semanal(reflexion_ejemplo)
        print("Reflexión semanal de ejemplo creada")
        
        print("\n✅ Datos de ejemplo creados exitosamente!")
        print(f"Puedes iniciar sesión con: demo@ejemplo.com")
        
    except Exception as e:
        print(f"❌ Error al crear datos de ejemplo: {e}")

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    dependencias = [
        'flask',
        'reportlab',
        'werkzeug'
    ]
    
    print("Verificando dependencias...")
    faltantes = []
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            faltantes.append(dep)
            print(f"❌ {dep}")
    
    if faltantes:
        print(f"\n⚠️  Dependencias faltantes: {', '.join(faltantes)}")
        print("Ejecuta: pip install -r requirements.txt")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def main():
    """Función principal de inicialización"""
    print("=" * 60)
    print("🌱 DIARIO DE ALIMENTACIÓN CONSCIENTE")
    print("   Mtra. Andrea Tagle Díaz - Nutrióloga Deportiva")
    print("=" * 60)
    print()
    
    # Verificar dependencias
    if not verificar_dependencias():
        sys.exit(1)
    
    print()
    
    # Inicializar base de datos
    print("Inicializando base de datos...")
    try:
        init_database()
        print("✅ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")
        sys.exit(1)
    
    print()
    
    # Crear datos de ejemplo
    crear_datos_ejemplo()
    
    print()
    print("=" * 60)
    print("🎉 ¡INICIALIZACIÓN COMPLETADA!")
    print()
    print("Para ejecutar la aplicación:")
    print("1. python app.py")
    print("2. Abre tu navegador en: http://localhost:5000")
    print()
    if os.path.exists('diario_alimentacion.db'):
        print("Base de datos creada en: diario_alimentacion.db")
    print("=" * 60)

if __name__ == "__main__":
    main()