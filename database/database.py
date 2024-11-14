import sqlite3
import os

DATABASE_NAME = "/var/lib/sqlite/database.db"  # Cambia según sea necesario para el contenedor

def create_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_connection():
    """Establece la conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_tables(conn):
    """Crea todas las tablas necesarias para la aplicación."""
    with conn:
        cursor = conn.cursor()
        
        # Creación de la tabla Medicos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Medicos (
                id_medico INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                especialidad TEXT NOT NULL,
                horarios_disponibles JSON NOT NULL
            );
        ''')
        
        # Creación de la tabla Pacientes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pacientes (
                id_paciente INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL,
                email TEXT NOT NULL,
                doctor_preferido INTEGER,
                FOREIGN KEY (doctor_preferido) REFERENCES Medicos(id_medico)
            );
        ''')
        
        # Creación de la tabla Agenda
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Agenda (
                id_agenda INTEGER PRIMARY KEY,
                id_medico INTEGER,
                id_cita INTEGER,
                FOREIGN KEY (id_medico) REFERENCES Medicos(id_medico),
                FOREIGN KEY (id_cita) REFERENCES Citas(id_cita)
            );
        ''')
        
        # Creación de la tabla Citas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Citas (
                id_cita INTEGER PRIMARY KEY,
                id_medico INTEGER,
                id_paciente INTEGER,
                fecha DATE NOT NULL,
                hora TIME NOT NULL,
                estado TEXT NOT NULL,
                asistio BOOLEAN,
                FOREIGN KEY (id_medico) REFERENCES Medicos(id_medico),
                FOREIGN KEY (id_paciente) REFERENCES Pacientes(id_paciente)
            );
        ''')
        
        # Creación de la tabla Notificaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Notificaciones (
                id_notificacion INTEGER PRIMARY KEY,
                id_cita INTEGER,
                tipo_notificacion TEXT NOT NULL,
                mensaje TEXT NOT NULL,
                FOREIGN KEY (id_cita) REFERENCES Citas(id_cita)
            );
        ''')

def reset_database():
    """Reinicia la base de datos eliminando y recreando el archivo database.db."""
    # Eliminar la base de datos existente si está presente
    if os.path.exists(DATABASE_NAME):
        os.remove(DATABASE_NAME)
    
    # Crear una nueva conexión y establecer las tablas
    conn = create_connection()
    create_tables(conn)
    conn.close()
    print("Base de datos reiniciada y tablas creadas.")

# Ejecutar el reset de la base de datos al iniciar
if __name__ == "__main__":
    reset_database()
