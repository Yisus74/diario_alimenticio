from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from database import DatabaseManager, init_database
from datetime import datetime, timedelta
import calendar
import json
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import os
import tempfile

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Cambiar en producción

# Configuración
app.config['UPLOAD_FOLDER'] = 'uploads'

# Inicializar la base de datos al importar el módulo
def init_app():
    """Inicializa la aplicación y la base de datos"""
    try:
        init_database()
        print("✅ Base de datos inicializada correctamente")
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")

# Ejecutar inicialización
init_app()

# Función segura para obtener atributos de un objeto
def safe_get_attr(obj, attr, default=None):
    try:
            return getattr(obj, attr, default)
    except Exception:
        return default

# Si también usas formateo de fechas, puedes agregar:
from datetime import datetime

def safe_format_date(value, fmt="%d/%m/%Y"):
    if isinstance(value, datetime):
        return value.strftime(fmt)
    try:
        return datetime.strptime(str(value), "%Y-%m-%d").strftime(fmt)
    except Exception:
        return value

# Registrar funciones en el entorno Jinja2
app.jinja_env.globals.update(
    safe_get_attr=safe_get_attr,
    safe_format_date=safe_format_date
)
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = DatabaseManager.obtener_usuario_por_email(email)
        if user:
            session['user_id'] = user['id']
            session['user_name'] = user['nombre']
            flash('Bienvenido de vuelta!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email no encontrado', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        
        # Verificar si el usuario ya existe
        existing_user = DatabaseManager.obtener_usuario_por_email(email)
        if existing_user:
            flash('El email ya está registrado', 'error')
            return render_template('register.html')
        
        # Crear nuevo usuario
        user_id = DatabaseManager.crear_usuario(nombre, email)
        session['user_id'] = user_id
        session['user_name'] = nombre
        flash('Registro exitoso! Bienvenido!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    
    try:
        # Obtener registros de la semana actual
        registros_semana = DatabaseManager.obtener_registros_por_usuario(
            user_id, week_start, today
        )
        
        # Obtener registros recientes (últimos 5)
        registros_recientes = DatabaseManager.obtener_registros_por_usuario(user_id)[:5]
       

        # Calcular estadísticas de la semana de manera segura
        consistencia_semanal = 0
        if registros_semana:
            consistencia_semanal = min((len(registros_semana) / 7) * 100, 100)
        
        return render_template('dashboard.html', 
                             registros_semana=registros_semana,
                             registros_recientes=registros_recientes,
                             today=today,
                             consistencia_semanal=int(consistencia_semanal))
    
    except Exception as e:
        print(f"Error en dashboard: {e}")
        flash('Error al cargar el dashboard. Intenta de nuevo.', 'error')
        return render_template('dashboard.html', 
                             registros_semana=[],
                             registros_recientes=[],
                             today=today,
                             consistencia_semanal=0)

@app.route('/nuevo_registro', methods=['GET', 'POST'])
def nuevo_registro():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        try:
            # Función auxiliar para manejar valores del formulario
            def get_form_value(key, default=''):
                value = request.form.get(key, default).strip()
                return value if value else None
            
            def get_form_int(key, default=None):
                value = request.form.get(key, '').strip()
                if not value:
                    return default
                try:
                    return int(value)
                except (ValueError, TypeError):
                    return default
            
            def get_form_bool(key):
                return key in request.form
            
            # Procesar datos del formulario de manera segura
            datos = {
                'usuario_id': session['user_id'],
                'fecha': get_form_value('fecha'),
                'que_comi': get_form_value('que_comi'),
                'donde_estaba': get_form_value('donde_estaba'),
                'con_quien': get_form_value('con_quien'),
                'nivel_hambre_antes': get_form_int('nivel_hambre_antes'),
                'nivel_saciedad_despues': get_form_int('nivel_saciedad_despues'),
                'emociones_antes': get_form_value('emociones_antes'),
                'sensaciones_fisicas_antes': get_form_value('sensaciones_fisicas_antes'),
                'emociones_despues': get_form_value('emociones_despues'),
                'comio_con_atencion': get_form_bool('comio_con_atencion'),
                'que_noto': get_form_value('que_noto'),
                'que_aprendio': get_form_value('que_aprendio')
            }
            
            # Validar campos requeridos
            if not datos['fecha'] or not datos['que_comi']:
                flash('La fecha y "¿Qué comí?" son campos obligatorios.', 'error')
                emociones = DatabaseManager.obtener_emociones()
                return render_template('nuevo_registro.html', 
                                     emociones=emociones,
                                     today=datetime.now().date())
            
            # Crear registro
            registro_id = DatabaseManager.crear_registro_diario(datos)
            flash('Registro guardado exitosamente!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            print(f"Error creando registro: {e}")
            flash('Error al guardar el registro. Intenta de nuevo.', 'error')
    
    # GET request - mostrar formulario
    emociones = DatabaseManager.obtener_emociones()
    return render_template('nuevo_registro.html', 
                         emociones=emociones,
                         today=datetime.now().date())

@app.route('/mis_registros')
def mis_registros():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    # Filtros opcionales
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin = request.args.get('fecha_fin')
    
    try:
        if fecha_inicio and fecha_fin:
            registros = DatabaseManager.obtener_registros_por_usuario(
                user_id, fecha_inicio, fecha_fin
            )
        else:
            registros = DatabaseManager.obtener_registros_por_usuario(user_id)
        
        # Función auxiliar para manejar objetos Row
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
        
        # Calcular estadísticas de manera segura
        estadisticas = {
            'total_registros': len(registros),
            'promedio_hambre': 0,
            'promedio_saciedad': 0,
            'porcentaje_atencion': 0
        }
        
        if registros:
            # Función auxiliar para valores seguros
            def safe_float(value, default=0.0):
                if value is None:
                    return default
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return default
            
            # Calcular promedios
            niveles_hambre = []
            niveles_saciedad = []
            registros_con_atencion = 0
            
            for r in registros:
                # Hambre
                hambre = safe_get(r, 'nivel_hambre_antes')
                if hambre is not None:
                    hambre_float = safe_float(hambre)
                    if 0 <= hambre_float <= 10:
                        niveles_hambre.append(hambre_float)
                
                # Saciedad
                saciedad = safe_get(r, 'nivel_saciedad_despues')
                if saciedad is not None:
                    saciedad_float = safe_float(saciedad)
                    if 0 <= saciedad_float <= 10:
                        niveles_saciedad.append(saciedad_float)
                
                # Atención
                if safe_get(r, 'comio_con_atencion'):
                    registros_con_atencion += 1
            
            # Calcular estadísticas finales
            if niveles_hambre:
                estadisticas['promedio_hambre'] = sum(niveles_hambre) / len(niveles_hambre)
            
            if niveles_saciedad:
                estadisticas['promedio_saciedad'] = sum(niveles_saciedad) / len(niveles_saciedad)
            
            estadisticas['porcentaje_atencion'] = (registros_con_atencion / len(registros)) * 100
        datos= []
        for fila in registros:
            datos.append(dict(fila))
        return render_template('mis_registros.html', 
                             registros=datos, 
                             estadisticas=estadisticas)
    
    except Exception as e:
        print(f"Error en mis_registros: {e}")
        flash('Error al cargar los registros. Intenta de nuevo.', 'error')
        return render_template('mis_registros.html', 
                             registros=[], 
                             estadisticas={'total_registros': 0, 'promedio_hambre': 0, 'promedio_saciedad': 0, 'porcentaje_atencion': 0})

@app.route('/reflexion_semanal', methods=['GET', 'POST'])
def reflexion_semanal():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        today = datetime.now().date()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        datos = {
            'usuario_id': session['user_id'],
            'semana_inicio': week_start,
            'semana_fin': week_end,
            'patrones_observados': request.form['patrones_observados'],
            'momentos_sin_hambre': request.form['momentos_sin_hambre'],
            'comidas_disfrutadas': request.form['comidas_disfrutadas'],
            'que_tenian_comun': request.form['que_tenian_comun'],
            'que_mejorar': request.form['que_mejorar']
        }
        
        DatabaseManager.crear_reflexion_semanal(datos)
        flash('Reflexión semanal guardada exitosamente!', 'success')
        return redirect(url_for('dashboard'))
    
    # Obtener registros de la semana actual para ayudar en la reflexión
    user_id = session['user_id']
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())
    
    registros_semana = DatabaseManager.obtener_registros_por_usuario(
        user_id, week_start, today
    )
    
    return render_template('reflexion_semanal.html', registros_semana=registros_semana)

@app.route('/mis_reflexiones')
def mis_reflexiones():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    reflexiones = DatabaseManager.obtener_reflexiones_por_usuario(user_id)
    
    return render_template('mis_reflexiones.html', reflexiones=reflexiones)

@app.route('/generar_reporte_mensual')
def generar_reporte_mensual():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    
    # Calcular el primer y último día del mes
    primer_dia = datetime(year, month, 1).date()
    ultimo_dia = datetime(year, month, calendar.monthrange(year, month)[1]).date()
    
    # Obtener registros del mes
    registros = DatabaseManager.obtener_registros_por_usuario(
        user_id, primer_dia, ultimo_dia
    )
    
    # Generar PDF
    filename = f"reporte_mensual_{year}_{month:02d}.pdf"
    filepath = os.path.join(tempfile.gettempdir(), filename)
    
    generar_pdf_reporte(filepath, registros, session['user_name'], year, month)
    
    return send_file(filepath, as_attachment=True, download_name=filename)

def generar_pdf_reporte(filepath, registros, usuario_nombre, year, month):
    """Genera un reporte PDF con todos los registros del mes"""
    doc = SimpleDocTemplate(filepath, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Función auxiliar para manejar objetos Row
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
    
    # Título
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        textColor=HexColor('#2D5A41'),
        alignment=1
    )
    
    mes_nombre = calendar.month_name[month]
    title = Paragraph(f"Reporte Mensual de Alimentación Consciente<br/>{mes_nombre} {year}<br/>Usuario: {usuario_nombre}", title_style)
    story.append(title)
    story.append(Spacer(1, 20))
    
    # Resumen estadístico
    if registros:
        total_registros = len(registros)
        
        # Calcular promedios de manera segura
        def safe_float(value, default=0.0):
            if value is None:
                return default
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        
        # Filtrar valores válidos para hambre
        niveles_hambre = []
        for r in registros:
            hambre = safe_get(r, 'nivel_hambre_antes')
            if hambre is not None:
                hambre_float = safe_float(hambre)
                if 0 <= hambre_float <= 10:
                    niveles_hambre.append(hambre_float)
        
        # Filtrar valores válidos para saciedad
        niveles_saciedad = []
        for r in registros:
            saciedad = safe_get(r, 'nivel_saciedad_despues')
            if saciedad is not None:
                saciedad_float = safe_float(saciedad)
                if 0 <= saciedad_float <= 10:
                    niveles_saciedad.append(saciedad_float)
        
        # Calcular promedios
        promedio_hambre = sum(niveles_hambre) / len(niveles_hambre) if niveles_hambre else 0
        promedio_saciedad = sum(niveles_saciedad) / len(niveles_saciedad) if niveles_saciedad else 0
        
        # Contar días únicos
        fechas_unicas = set()
        for r in registros:
            fecha = safe_get(r, 'fecha')
            if fecha:
                fechas_unicas.add(str(fecha))
        
        resumen_data = [
            ['Métrica', 'Valor'],
            ['Total de registros', str(total_registros)],
            ['Promedio nivel de hambre', f"{promedio_hambre:.1f}/10" if promedio_hambre > 0 else "N/A"],
            ['Promedio nivel de saciedad', f"{promedio_saciedad:.1f}/10" if promedio_saciedad > 0 else "N/A"],
            ['Días con registro', str(len(fechas_unicas))]
        ]
        
        resumen_table = Table(resumen_data, colWidths=[3*inch, 2*inch])
        resumen_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor('#4A6741')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#F0F8F0')),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(Paragraph("Resumen del Mes", styles['Heading2']))
        story.append(resumen_table)
        story.append(Spacer(1, 20))
        
        # Registros detallados
        story.append(Paragraph("Registros Diarios Detallados", styles['Heading2']))
        story.append(Spacer(1, 10))
        
        for registro in reversed(registros):  # Mostrar del más antiguo al más reciente
            try:
                fecha_str = str(safe_get(registro, 'fecha', 'N/A'))
                if fecha_str != 'N/A':
                    try:
                        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').strftime('%d/%m/%Y')
                    except:
                        fecha = fecha_str
                else:
                    fecha = 'N/A'
                
                # Manejar valores None de manera segura
                def safe_str(value, default=''):
                    return str(value) if value is not None else default
                
                def safe_bool_str(value):
                    if value is None:
                        return 'No especificado'
                    return 'Sí' if value else 'No'
                
                registro_data = [
                    ['Fecha', fecha],
                    ['¿Qué comí?', safe_str(safe_get(registro, 'que_comi'), 'No especificado')],
                    ['¿Dónde estaba?', safe_str(safe_get(registro, 'donde_estaba'), 'No especificado')],
                    ['¿Con quién?', safe_str(safe_get(registro, 'con_quien'), 'No especificado')],
                    ['Nivel de hambre (0-10)', safe_str(safe_get(registro, 'nivel_hambre_antes'), 'No especificado')],
                    ['Nivel de saciedad (0-10)', safe_str(safe_get(registro, 'nivel_saciedad_despues'), 'No especificado')],
                    ['Emociones antes', safe_str(safe_get(registro, 'emociones_antes'), 'No especificado')],
                    ['Sensaciones físicas antes', safe_str(safe_get(registro, 'sensaciones_fisicas_antes'), 'No especificado')],
                    ['Emociones después', safe_str(safe_get(registro, 'emociones_despues'), 'No especificado')],
                    ['¿Comió con atención?', safe_bool_str(safe_get(registro, 'comio_con_atencion'))],
                    ['¿Qué notó?', safe_str(safe_get(registro, 'que_noto'), 'No especificado')],
                    ['¿Qué aprendió?', safe_str(safe_get(registro, 'que_aprendio'), 'No especificado')]
                ]
                
                registro_table = Table(registro_data, colWidths=[2.5*inch, 4*inch])
                registro_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), HexColor('#E8F5E8')),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, HexColor('#F9FDF9')])
                ]))
                
                story.append(registro_table)
                story.append(Spacer(1, 15))
                
            except Exception as e:
                print(f"Error procesando registro para PDF: {e}")
                continue
    
    else:
        story.append(Paragraph("No hay registros para este mes.", styles['Normal']))
    
    try:
        doc.build(story)
    except Exception as e:
        print(f"Error generando PDF: {e}")
        raise

@app.route('/estadisticas')
def estadisticas():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    
    try:
        # Obtener todos los registros para estadísticas
        registros = DatabaseManager.obtener_registros_por_usuario(user_id)
        
        # Inicializar estadísticas
        stats = {
            'total_registros': 0,
            'promedio_hambre': 0,
            'promedio_saciedad': 0,
            'dias_consecutivos': 0,
            'emociones_frecuentes': {},
            'registros_con_atencion': 0,
            'porcentaje_atencion': 0
        }
        
        if not registros:
            return render_template('estadisticas.html', stats=stats, registros=[], registros_json=[])
        
        stats['total_registros'] = len(registros)
        
        # Función auxiliar para convertir Row a dict y obtener valores seguros
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
        
        def safe_float(value, default=0.0):
            if value is None:
                return default
            try:
                return float(value)
            except (ValueError, TypeError):
                return default
        
        # Calcular promedios de manera segura
        try:
            niveles_hambre = []
            niveles_saciedad = []
            registros_con_atencion = 0
            
            for r in registros:
                # Niveles de hambre - usar safe_get en lugar de get
                hambre_value = safe_get(r, 'nivel_hambre_antes')
                if hambre_value is not None:
                    hambre_float = safe_float(hambre_value)
                    if 0 <= hambre_float <= 10:
                        niveles_hambre.append(hambre_float)
                
                # Niveles de saciedad - usar safe_get en lugar de get
                saciedad_value = safe_get(r, 'nivel_saciedad_despues')
                if saciedad_value is not None:
                    saciedad_float = safe_float(saciedad_value)
                    if 0 <= saciedad_float <= 10:
                        niveles_saciedad.append(saciedad_float)
                
                # Contar registros con atención - usar safe_get
                atencion_value = safe_get(r, 'comio_con_atencion')
                if atencion_value is not None and atencion_value:
                    registros_con_atencion += 1
            
            # Calcular promedios solo si hay datos válidos
            if niveles_hambre:
                stats['promedio_hambre'] = sum(niveles_hambre) / len(niveles_hambre)
            
            if niveles_saciedad:
                stats['promedio_saciedad'] = sum(niveles_saciedad) / len(niveles_saciedad)
            
            stats['registros_con_atencion'] = registros_con_atencion
            if stats['total_registros'] > 0:
                stats['porcentaje_atencion'] = (registros_con_atencion / stats['total_registros']) * 100
            
        except Exception as e:
            print(f"Error calculando promedios: {e}")
        
        # Calcular días consecutivos de manera segura
        try:
            fechas_validas = []
            for r in registros:
                try:
                    fecha_value = safe_get(r, 'fecha')
                    if fecha_value:
                        if isinstance(fecha_value, str):
                            fecha = datetime.strptime(fecha_value, '%Y-%m-%d').date()
                        else:
                            fecha = fecha_value
                        fechas_validas.append(fecha)
                except (ValueError, TypeError, AttributeError):
                    continue
            
            if fechas_validas:
                fechas_ordenadas = sorted(list(set(fechas_validas)))
                if len(fechas_ordenadas) > 1:
                    max_consecutivos = 1
                    consecutivos_actuales = 1
                    
                    for i in range(1, len(fechas_ordenadas)):
                        try:
                            delta = (fechas_ordenadas[i] - fechas_ordenadas[i-1]).days
                            if delta == 1:
                                consecutivos_actuales += 1
                                max_consecutivos = max(max_consecutivos, consecutivos_actuales)
                            else:
                                consecutivos_actuales = 1
                        except (AttributeError, TypeError):
                            consecutivos_actuales = 1
                    
                    stats['dias_consecutivos'] = max_consecutivos
                else:
                    stats['dias_consecutivos'] = 1
                    
        except Exception as e:
            print(f"Error calculando días consecutivos: {e}")
            stats['dias_consecutivos'] = 0
        
        # Procesar emociones de manera segura
        try:
            todas_emociones = []
            for registro in registros:
                emociones_antes = safe_get(registro, 'emociones_antes')
                if emociones_antes and isinstance(emociones_antes, str) and emociones_antes.strip():
                    emociones_lista = []
                    for e in emociones_antes.split(','):
                        if e and e.strip():
                            emociones_lista.append(e.strip().lower())
                    todas_emociones.extend(emociones_lista)
            
            # Contar frecuencia de emociones
            emociones_count = {}
            for emocion in todas_emociones:
                if emocion:  # Asegurar que no sea vacío
                    emociones_count[emocion] = emociones_count.get(emocion, 0) + 1
            
            # Ordenar por frecuencia y tomar las top 10
            if emociones_count:
                stats['emociones_frecuentes'] = dict(
                    sorted(emociones_count.items(), key=lambda x: x[1], reverse=True)[:10]
                )
            
        except Exception as e:
            print(f"Error procesando emociones: {e}")
            stats['emociones_frecuentes'] = {}
        
        # Convertir registros a formato seguro para JSON
        registros_json = []
        for r in registros:
            try:
                registro_clean = {
                    'fecha': str(safe_get(r, 'fecha', '')),
                    'nivel_hambre_antes': safe_float(safe_get(r, 'nivel_hambre_antes'), 0),
                    'nivel_saciedad_despues': safe_float(safe_get(r, 'nivel_saciedad_despues'), 0),
                    'comio_con_atencion': bool(safe_get(r, 'comio_con_atencion', False))
                }
                registros_json.append(registro_clean)
            except Exception as e:
                print(f"Error procesando registro: {e}")
                continue
        
        return render_template('estadisticas.html', 
                             stats=stats, 
                             registros=registros, 
                             registros_json=registros_json)
    
    except Exception as e:
        print(f"Error general en estadísticas: {e}")
        flash('Error al cargar las estadísticas. Intenta de nuevo.', 'error')
        return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # Configuración de ejecución
    debug_mode = app.config.get('DEBUG', True)
    host = app.config.get('HOST', '127.0.0.1')
    port = app.config.get('PORT', 5000)
    
    print("🌱 Iniciando Diario de Alimentación Consciente...")
    print(f"📱 Aplicación disponible en: http://{host}:{port}")
    
    if debug_mode:
        print("⚡ Modo debug activado")
    
    try:
        app.run(debug=debug_mode, host=host, port=port)
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ El puerto {port} ya está en uso")
            print(f"💡 Intenta con otro puerto: python app.py")
            print(f"   O detén el proceso que usa el puerto {port}")
        else:
            print(f"❌ Error al iniciar la aplicación: {e}")
    except KeyboardInterrupt:
        print("\n👋 Aplicación detenida por el usuario")