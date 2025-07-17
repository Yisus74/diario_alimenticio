# Diario de Alimentación Consciente

Una aplicación web completa para llevar un diario de alimentación consciente basada en la metodología de la Mtra. Andrea Tagle Díaz, Nutrióloga Deportiva.

## 🌟 Características

- **Registro Diario**: Documenta qué comes, cómo te sientes y tu nivel de hambre/saciedad
- **Alimentación Consciente**: Enfoque en mindfulness y atención plena durante las comidas
- **Reflexiones Semanales**: Identifica patrones y establece objetivos de mejora
- **Estadísticas y Análisis**: Visualiza tu progreso con gráficos y métricas
- **Reportes PDF**: Genera reportes mensuales descargables
- **Interfaz Moderna**: Diseño responsivo con Tailwind CSS

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: SQLite
- **Frontend**: HTML5, Tailwind CSS, JavaScript
- **Gráficos**: Chart.js
- **PDF**: ReportLab
- **Iconos**: Font Awesome

## 📋 Requisitos Previos

- Python 3.7 o superior
- pip (administrador de paquetes de Python)

## 🚀 Instalación y Ejecución

### Opción 1: Arranque Automático (Más Fácil)

**En Windows:**
```bash
# Simplemente ejecuta el archivo por lotes
start.bat
```

**En macOS/Linux:**
```bash
# Dar permisos de ejecución y ejecutar
chmod +x start.sh
./start.sh
```

### Opción 2: Instalación Guiada (Recomendado)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar script de inicialización (opcional, crea datos de ejemplo)
python init.py

# 3. Ejecutar la aplicación con el script mejorado
python run.py
```

### Opción 3: Instalación Manual

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Inicializar base de datos
python -c "from database import init_database; init_database()"

# 3. Ejecutar aplicación
python app.py
```

### 4. Acceder a la Aplicación

La aplicación estará disponible en: `http://localhost:5000`

## 📁 Estructura del Proyecto

```
diario-alimentacion-consciente/
│
├── app.py                      # Aplicación principal Flask
├── database.py                 # Configuración de base de datos
├── config.py                   # Configuración de la aplicación
├── init.py                     # Script de inicialización
├── run.py                      # Script de ejecución mejorado
├── diagnostico.py              # 🔍 Herramienta de diagnóstico
├── reparar.py                  # 🔧 Herramienta de reparación automática
├── test_fixes.py               # 🧪 Script de pruebas de correcciones
├── test_row_fix.py             # 🧪 Prueba específica de objetos Row
├── verificar.py                # ⚡ Verificación rápida de errores
├── fix_filters.py              # 🔧 Corrector específico de filtros
├── start.bat                   # Arranque automático (Windows)
├── start.sh                    # Arranque automático (macOS/Linux)
├── requirements.txt            # Dependencias Python
├── README.md                   # Este archivo
│
├── templates/                  # Plantillas HTML
│   ├── base.html              # Plantilla base
│   ├── login.html             # Página de login/registro
│   ├── register.html          # Página de registro
│   ├── dashboard.html         # Panel principal
│   ├── nuevo_registro.html    # Formulario de nuevo registro
│   ├── mis_registros.html     # Lista de registros
│   ├── reflexion_semanal.html # Reflexión semanal
│   ├── mis_reflexiones.html   # Lista de reflexiones
│   └── estadisticas.html      # Estadísticas y gráficos
│
├── uploads/                    # Directorio de archivos (se crea automáticamente)
└── diario_alimentacion.db     # Base de datos SQLite (se crea automáticamente)
```

## 🛠️ Herramientas de Diagnóstico y Reparación

### ⚡ Verificación Rápida (NUEVO)
```bash
python verificar.py
```
- Verificación ultra-rápida de errores comunes
- Prueba filtros de Jinja2
- Valida importaciones básicas
- Perfecto para verificar correcciones específicas

### 🔧 Corrector de Filtros (NUEVO)
```bash
python fix_filters.py
```
- Soluciona específicamente errores de filtros de Jinja2
- Registra filtros manualmente si fallan los decoradores
- Verificación y corrección automática
- Ideal para el error "No filter named 'safe_selectattr' found"

### 🧪 Verificación de Correcciones
```bash
python test_fixes.py
```
- Verifica que el error TypeError esté corregido
- Prueba operaciones con valores None
- Valida filtros seguros de plantillas
- Confirma que los cálculos funcionan correctamente

### 🔍 Diagnóstico Automático
```bash
python diagnostico.py
```
- Verifica que todos los archivos estén presentes
- Comprueba las dependencias instaladas
- Analiza el estado de la base de datos
- Detecta problemas de configuración
- Genera un reporte completo

### 🔧 Reparación Automática
```bash
python reparar.py
```
**Opciones disponibles:**
1. **Reparación completa** (recomendado) - Soluciona todos los problemas
2. **Solo reinstalar dependencias** - Reinstala Flask, ReportLab, etc.
3. **Solo reparar base de datos** - Recrea la base de datos
4. **Solo verificar Flask** - Actualiza Flask si es necesario
5. **Solo limpiar cache** - Elimina archivos temporales
6. **Crear directorios faltantes** - Crea carpetas necesarias
7. **Ejecutar diagnóstico** - Ejecuta diagnóstico completo
8. **Verificación rápida** - Ejecuta verificación rápida

### 🚨 En caso de errores:
1. **Primero**: `python verificar.py` (verificación ultra-rápida)
2. **Segundo**: `python fix_filters.py` (específico para filtros)
3. **Tercero**: `python test_fixes.py` (verifica correcciones específicas)
4. **Cuarto**: `python diagnostico.py` (identifica otros problemas)
5. **Quinto**: `python reparar.py` → Opción 1 (soluciona automáticamente)
6. **Sexto**: `python run.py` (ejecuta la aplicación)

## 🎯 Uso de la Aplicación

### 1. Registro e Inicio de Sesión
- Crea una cuenta con tu nombre y email
- Inicia sesión para acceder a tu diario personal

### 2. Crear Registros Diarios
- Documenta qué comiste, dónde y con quién
- Registra tus niveles de hambre (0-10) antes de comer
- Registra tu nivel de saciedad (0-10) después de comer
- Selecciona las emociones que sentiste antes de comer
- Reflexiona sobre la experiencia y qué aprendiste

### 3. Reflexiones Semanales
- Al final de cada semana, completa una reflexión
- Identifica patrones en tu alimentación y emociones
- Establece objetivos para la siguiente semana

### 4. Seguimiento y Análisis
- Revisa tus estadísticas en el panel de control
- Genera reportes PDF mensuales
- Visualiza tendencias en gráficos interactivos

## 🔧 Configuración Avanzada

### Cambiar la Clave Secreta
En `app.py`, cambia la línea:
```python
app.secret_key = 'tu_clave_secreta_aqui'
```

### Configurar para Producción
Para uso en producción, considera:
- Usar una base de datos más robusta (PostgreSQL, MySQL)
- Configurar variables de entorno para la clave secreta
- Usar un servidor web como Gunicorn
- Configurar HTTPS

## 📊 Funcionalidades Detalladas

### Registro Diario
- **Información básica**: Fecha, alimentos consumidos, ubicación, compañía
- **Niveles de hambre/saciedad**: Escala de 0-10 con sliders interactivos
- **Emociones**: Selección múltiple de emociones predefinidas
- **Atención plena**: Checkbox para indicar si comió con atención
- **Reflexiones**: Campos de texto para observaciones y aprendizajes

### Reflexión Semanal
- **Análisis de patrones**: Identificación de comportamientos recurrentes
- **Momentos sin hambre**: Reflexión sobre comer emocional
- **Comidas disfrutadas**: Qué las hizo especiales
- **Objetivos futuros**: Planes de mejora para la siguiente semana

### Estadísticas
- **Métricas generales**: Total de registros, promedios, rachas
- **Gráficos de tendencias**: Niveles de hambre y saciedad en el tiempo
- **Análisis de emociones**: Frecuencia de emociones antes de comer
- **Patrones semanales**: Actividad por día de la semana

### Reportes PDF
- **Resumen mensual**: Estadísticas del mes
- **Registros detallados**: Todos los registros del período
- **Formato profesional**: Layout diseñado para fácil lectura

## 🤝 Contribuir

Si deseas contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está basado en la metodología de alimentación consciente de la Mtra. Andrea Tagle Díaz, Nutrióloga Deportiva.

## 🆘 Soporte

Si encuentras algún problema:
1. Verifica que todas las dependencias estén instaladas correctamente
2. Asegúrate de que Python 3.7+ esté instalado
3. Revisa que el puerto 5000 no esté siendo usado por otra aplicación

### Problemas Comunes

**Error al instalar reportlab**:
```bash
# En Windows, puede necesitar Microsoft C++ Build Tools
# En macOS, asegúrate de tener Xcode Command Line Tools
# En Linux, instala python3-dev
sudo apt-get install python3-dev  # Ubuntu/Debian
```

**Puerto 5000 ocupado**:
```python
# En app.py, cambia la última línea a:
app.run(debug=True, port=5001)
```

**Base de datos no se crea**:
```bash
# Ejecuta manualmente:
python -c "from database import init_database; init_database()"
```

## 🙏 Agradecimientos

- Mtra. Andrea Tagle Díaz por la metodología de alimentación consciente
- Comunidad de Flask por el excelente framework
- Tailwind CSS por el sistema de diseño
- Font Awesome por los iconos

---

**¡Esperamos que esta aplicación te ayude en tu viaje hacia una alimentación más consciente! 🌱**