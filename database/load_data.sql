COPY Pacientes (id_paciente, nombre, telefono, email)
FROM '/docker-entrypoint-initdb.d/pacientes.csv'
DELIMITER ','
CSV HEADER;