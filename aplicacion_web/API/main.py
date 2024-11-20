# from app import app
from aplicacion_web.API.models import Medico, Paciente, Cita, Notificacion
from aplicacion_web.API import db
from aplicacion_web.API import create_app
from flask import Flask, make_response, jsonify, request

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)


# @app.route('/')
# def test():
#     return make_response(jsonify({'message': 'test route'}), 200)

# # Traer a todos los medicos
# @app.route('/medicos', methods=['GET'])
# def get_medicos():
#     try:
#         medicos = Medico.query.all()  # Nos permite traer todos los usuarios
#         return make_response(
#             jsonify({
#                 'message': 'Medicos encontrados',
#                 'medicos': [medico.json() for medico in medicos]
#             }), 200)
#     except Exception as e:
#         return make_response(
#             jsonify({'message': 'Exception al traer los medicos'}), 500)

# # Crear Medico
# @app.route('/crear_medico', methods=['POST'])
# def crear_medico():
#     try:
#         data = request.get_json()
#         nuevo_medico = Medico(
#             nombre=data['nombre'],
#             especialidad=data['especialidad'],
#             horarios_disponibles=data['horarios_disponibles'])

#         db.session.add(nuevo_medico)
#         db.session.commit()

#         return make_response(jsonify({'message': 'Medico creado'}), 201)
#     except Exception as e:
#         return make_response(jsonify({'message': 'Exception al crear el medico'}),500)


# # Traer a un medico por id
# @app.route('/medicos/<int:medico_id>', methods=['GET'])
# def get_medico(medico_id):
#     try:
#         medico = Medico.query.filter_by(medico_id=medico_id).first()
#         if medico:
#             return make_response(jsonify({'Medico': medico.json()}), 200)
#         else:
#             return make_response(jsonify({'message': 'Medico no encontrado'}),404)
#     except Exception as e:
#         return make_response(jsonify({'message': 'Exception al traer al medico'}),500)


# # Actualizar datos de un medico por id
# @app.route('/medicos/<int:medico_id>', methods=['PUT'])
# def actualizar_medico(medico_id):
#     try:
#         data = request.get_json()
#         if data:
#             medico = Medico.query.filter_by(medico_id=medico_id).first()
#             medico.nombre = data['nombre']
#             medico.especialidad = data['especialidad']
#             medico.horarios_disponibles = data['horarios_disponibles']
#             db.session.commit()
#             return make_response(jsonify({'message': 'Medico actualizado'}),200)
#         return make_response(jsonify({'message': 'Medico no encontrado'}), 404)
#     except Exception as e:
#         return make_response(
#             jsonify({'message': 'Exception al traer los medicos'}), 500)


# # Eliminar un medico por id
# @app.route('/medicos/<int:medico>id', methods=['DELETE'])
# def eliminar_medico(medico_id):
#     try:
#         medico = Medico.query.filter_by(medico_id=medico_id).first()
#         if medico:
#             db.session.delete(medico)
#             db.session.commit()
#             return make_response(jsonify({'message': 'Medico eliminado'}), 200)
#         return make_response(jsonify({'message': 'Medico no encontrado'}), 404)
#     except Exception as e:
#         return make_response(
#             jsonify({'message': 'Exception al traer los medicos'}), 500)
