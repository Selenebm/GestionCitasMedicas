-- Crear tabla Medicos
CREATE TABLE IF NOT EXISTS Medicos (
    id_medico INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    especialidad TEXT NOT NULL,
    horarios_disponibles TEXT[] NOT NULL
);

-- Crear tabla Pacientes
CREATE TABLE IF NOT EXISTS Pacientes (
    id_paciente SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    doctor_preferido INTEGER REFERENCES Medicos(id_medico)
);

-- Crear tabla Citas
CREATE TABLE IF NOT EXISTS Citas (
    id_cita SERIAL PRIMARY KEY,
    id_medico INTEGER REFERENCES Medicos(id_medico),
    id_paciente INTEGER REFERENCES Pacientes(id_paciente),
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado TEXT NOT NULL,
    asistio BOOLEAN
);

-- Crear tabla Notificaciones
CREATE TABLE IF NOT EXISTS Notificaciones (
    id_notificacion SERIAL PRIMARY KEY,
    id_cita INTEGER REFERENCES Citas(id_cita),
    tipo_notificacion TEXT NOT NULL,
    mensaje TEXT NOT NULL,
    fecha_envio DATE
);