from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from app import config
from models.medico import Medico
from models.paciente import Paciente
from models.cita import Cita
from models.notificacion import Notificacion
from os import environ, error

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
db = SQLAlchemy(app)


@app.route('/')
def test():
    return make_response(jsonify({'message': 'test route'}), 200)


# Crear Medico
@app.route('/crear_medico', methods=['POST'])
def crear_medico():
    try:
        data = request.get_json()
        nuevo_medico = Medico(
            nombre=data['nombre'],
            especialidad=data['especialidad'],
            horarios_disponibles=data['horarios_disponibles'])

        db.session.add(nuevo_medico)
        db.session.commit()

        return make_response(jsonify({'message': 'Medico creado'}), 201)
    except error:
        return make_response(jsonify({'message': 'Error al crear el medico'}),
                            500)


# Traer a todos los medicos
@app.route('/medicos', methods=['GET'])
def get_medicos():
    try:
        medicos = Medico.query.all()  # Nos permite traer todos los usuarios
        return make_response(
            jsonify({
                'message': 'Medicos encontrados',
                'medicos': [medico.json() for medico in medicos]
            }), 200)
    except error:
        return make_response(
            jsonify({'message': 'Error al traer los medicos'}), 500)


# Traer a un medico por id
@app.route('/medicos/<int:medico_id>', methods=['GET'])
def get_medico(medico_id):
    try:
        medico = Medico.query.filter_by(medico_id=medico_id).first()
        if medico:
            return make_response(jsonify({'Medico': medico.json()}), 200)
        else:
            return make_response(jsonify({'message': 'Medico no encontrado'}),
                                404)
    except error as e:
        return make_response(jsonify({'message': 'Error al traer al medico'}),500)


# Actualizar datos de un medico por id
@app.route('/medicos/<int:medico_id>', methods=['PUT'])
def actualizar_medico(medico_id):
    try:
        data = request.get_json()
        if data:
            medico = Medico.query.filter_by(medico_id=medico_id).first()
            medico.nombre = data['nombre']
            medico.especialidad = data['especialidad']
            medico.horarios_disponibles = data['horarios_disponibles']
            db.session.commit()
            return make_response(jsonify({'message': 'Medico actualizado'}),
                                200)
        return make_response(jsonify({'message': 'Medico no encontrado'}), 404)
    except error:
        return make_response(
            jsonify({'message': 'Error al traer los medicos'}), 500)


# Eliminar un medico por id
@app.route('/medicos/<int:medico>id', methods=['DELETE'])
def eliminar_medico(medico_id):
    try:
        medico = Medico.query.filter_by(medico_id=medico_id).first()
        if medico:
            db.session.delete(medico)
            db.session.commit()
            return make_response(jsonify({'message': 'Medico eliminado'}), 200)
        return make_response(jsonify({'message': 'Medico no encontrado'}), 404)
    except error:
        return make_response(
            jsonify({'message': 'Error al traer los medicos'}), 500)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
