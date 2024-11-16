-- Crear tabla Medicos
CREATE TABLE IF NOT EXISTS Medicos (
    id_medico SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    especialidad TEXT NOT NULL,
    horarios_disponibles JSONB NOT NULL
);

-- Crear tabla Pacientes
CREATE TABLE IF NOT EXISTS Pacientes (
    id_paciente INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    telefono TEXT NOT NULL,
    email TEXT NOT NULL,
    doctor_preferido INTEGER DEFAULT NULL,
    CONSTRAINT fk_doctor_preferido FOREIGN KEY (doctor_preferido) REFERENCES Medicos (id_medico)
);

-- Crear tabla Citas
CREATE TABLE IF NOT EXISTS Citas (
    id_cita SERIAL PRIMARY KEY,
    id_medico INTEGER,
    id_paciente INTEGER,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado TEXT NOT NULL,
    asistio BOOLEAN,
    CONSTRAINT fk_medico FOREIGN KEY (id_medico) REFERENCES Medicos (id_medico),
    CONSTRAINT fk_paciente FOREIGN KEY (id_paciente) REFERENCES Pacientes (id_paciente)
);

-- Crear tabla Notificaciones
CREATE TABLE IF NOT EXISTS Notificaciones (
    id_notificacion SERIAL PRIMARY KEY,
    id_cita INTEGER,
    tipo_notificacion TEXT NOT NULL,
    mensaje TEXT NOT NULL,
    CONSTRAINT fk_cita FOREIGN KEY (id_cita) REFERENCES Citas (id_cita)
);

-- Crear tabla Agenda
CREATE TABLE IF NOT EXISTS Agenda (
    id_agenda SERIAL PRIMARY KEY,
    id_medico INTEGER,
    id_cita INTEGER,
    CONSTRAINT fk_medico FOREIGN KEY (id_medico) REFERENCES Medicos (id_medico),
    CONSTRAINT fk_cita FOREIGN KEY (id_cita) REFERENCES Citas (id_cita)
);
