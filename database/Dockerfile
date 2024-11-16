#Imagen de la base de datos a usar
FROM postgres:13-alpine

# Montar la base de datos al contenedor
COPY init.sql /docker-entrypoint-initdb.d/
COPY pacientes.csv /docker-entrypoint-initdb.d/
COPY load_data.sql /docker-entrypoint-initdb.d/