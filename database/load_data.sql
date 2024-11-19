COPY Medicos (id_medico, nombre, especialidad, horarios_disponibles)
FROM '/docker-entrypoint-initdb.d/medicos.csv'
DELIMITER ','
CSV HEADER;

COPY Pacientes (id_paciente, nombre, telefono, email, doctor_preferido)
FROM '/docker-entrypoint-initdb.d/pacientes.csv'
DELIMITER ','
CSV HEADER;

COPY Citas (id_medico, id_paciente, fecha, hora, estado, asistio)
FROM '/docker-entrypoint-initdb.d/citas.csv'
DELIMITER ','
CSV HEADER;
