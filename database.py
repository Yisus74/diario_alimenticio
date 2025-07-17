import sqlite3
import datetime
from contextlib import contextmanager

DATABASE = 'diario_alimentacion.db'

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

def init_database():
    """Inicializa la base de datos con todas las tablas necesarias"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Tabla de usuarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de emociones predefinidas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emociones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE
            )
        ''')
        
        # Tabla de registros diarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registros_diarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                fecha DATE NOT NULL,
                que_comi TEXT NOT NULL,
                donde_estaba TEXT,
                con_quien TEXT,
                nivel_hambre_antes INTEGER CHECK(nivel_hambre_antes >= 0 AND nivel_hambre_antes <= 10),
                nivel_saciedad_despues INTEGER CHECK(nivel_saciedad_despues >= 0 AND nivel_saciedad_despues <= 10),
                emociones_antes TEXT,
                sensaciones_fisicas_antes TEXT,
                emociones_despues TEXT,
                comio_con_atencion BOOLEAN,
                que_noto TEXT,
                que_aprendio TEXT,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        # Tabla de emociones por registro
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registro_emociones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                registro_id INTEGER NOT NULL,
                emocion_id INTEGER NOT NULL,
                momento TEXT CHECK(momento IN ('antes', 'despues')),
                FOREIGN KEY (registro_id) REFERENCES registros_diarios (id),
                FOREIGN KEY (emocion_id) REFERENCES emociones (id)
            )
        ''')
        
        # Tabla de reflexiones semanales
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reflexiones_semanales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                semana_inicio DATE NOT NULL,
                semana_fin DATE NOT NULL,
                patrones_observados TEXT,
                momentos_sin_hambre TEXT,
                comidas_disfrutadas TEXT,
                que_tenian_comun TEXT,
                que_mejorar TEXT,
                fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
            )
        ''')
        
        # Insertar emociones predefinidas
        emociones_list = [
            'enojado', 'molesto', 'ansioso', 'avergonzado', 'torpe', 'valiente',
            'calmado', 'alegre', 'frío', 'confundido', 'desanimado', 'disgustado',
            'distraído', 'apenado', 'emocionado', 'amigable', 'culpable', 'feliz',
            'esperanzado', 'celoso', 'solo', 'amado', 'nervioso', 'ofendido',
            'espantado', 'pensativo', 'cansado', 'incómodo', 'inseguro', 'preocupado'
        ]
        
        for emocion in emociones_list:
            cursor.execute('INSERT OR IGNORE INTO emociones (nombre) VALUES (?)', (emocion,))
        
        conn.commit()

class DatabaseManager:
    @staticmethod
    def crear_usuario(nombre, email):
        """Crea un nuevo usuario"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO usuarios (nombre, email) VALUES (?, ?)',
                (nombre, email)
            )
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def obtener_usuario_por_email(email):
        """Obtiene un usuario por email"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
            return cursor.fetchone()
    
    @staticmethod
    def crear_registro_diario(datos):
        """Crea un registro diario"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO registros_diarios (
                    usuario_id, fecha, que_comi, donde_estaba, con_quien,
                    nivel_hambre_antes, nivel_saciedad_despues, emociones_antes,
                    sensaciones_fisicas_antes, emociones_despues, comio_con_atencion,
                    que_noto, que_aprendio
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos['usuario_id'], datos['fecha'], datos['que_comi'],
                datos['donde_estaba'], datos['con_quien'], datos['nivel_hambre_antes'],
                datos['nivel_saciedad_despues'], datos['emociones_antes'],
                datos['sensaciones_fisicas_antes'], datos['emociones_despues'],
                datos['comio_con_atencion'], datos['que_noto'], datos['que_aprendio']
            ))
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def obtener_registros_por_usuario(usuario_id, fecha_inicio=None, fecha_fin=None):
        """Obtiene registros de un usuario en un rango de fechas"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if fecha_inicio and fecha_fin:
                cursor.execute('''
                    SELECT * FROM registros_diarios 
                    WHERE usuario_id = ? AND fecha BETWEEN ? AND ?
                    ORDER BY fecha DESC
                ''', (usuario_id, fecha_inicio, fecha_fin))
            else:
                cursor.execute('''
                    SELECT * FROM registros_diarios 
                    WHERE usuario_id = ?
                    ORDER BY fecha DESC
                ''', (usuario_id,))
            return cursor.fetchall()
    
    @staticmethod
    def obtener_emociones():
        """Obtiene todas las emociones disponibles"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM emociones ORDER BY nombre')
            return cursor.fetchall()
    
    @staticmethod
    def crear_reflexion_semanal(datos):
        """Crea una reflexión semanal"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO reflexiones_semanales (
                    usuario_id, semana_inicio, semana_fin, patrones_observados,
                    momentos_sin_hambre, comidas_disfrutadas, que_tenian_comun,
                    que_mejorar
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datos['usuario_id'], datos['semana_inicio'], datos['semana_fin'],
                datos['patrones_observados'], datos['momentos_sin_hambre'],
                datos['comidas_disfrutadas'], datos['que_tenian_comun'],
                datos['que_mejorar']
            ))
            conn.commit()
            return cursor.lastrowid
    
    @staticmethod
    def obtener_reflexiones_por_usuario(usuario_id):
        """Obtiene reflexiones semanales de un usuario"""
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM reflexiones_semanales 
                WHERE usuario_id = ?
                ORDER BY semana_inicio DESC
            ''', (usuario_id,))
            return cursor.fetchall()

if __name__ == '__main__':
    init_database()
    print("Base de datos inicializada correctamente")