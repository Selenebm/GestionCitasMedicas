from flask import Flask, render_template, request, jsonify, make_response, Response
from models import db, Medico, Paciente, Cita, Notificacion
from datetime import datetime
from __init__ import create_app
import json
import pandas as pd
import os
from flask import send_file, current_app

app = create_app()

# Ruta de prueba
@app.route('/')
def test():
    return make_response(jsonify({'message': 'Ruta de prueba'}), 200)

# Renderizado del frontend
@app.route('/citas')
def citas():
    return render_template('citas.html')

@app.route('/pacientes')
def pacientes():
    return render_template('pacientes.html')


@app.route('/medicos')
def medicos():
    medicos = Medico.query.all()
    return render_template("medicos.html", medicos=medicos)

@app.route('/medicos', methods=['GET'])
def get_medicos():

    try:
        medicos = Medico.query.all()
        return make_json_response({
            'message': 'Médicos encontrados',
            'medicos': [medico.json() for medico in medicos]
        })
    except Exception as e:
        return make_json_response({'message': 'Error al acceder a la base de datos', 'error': str(e)}, status=500)


@app.route('/reporte')
def reportes():
    return render_template('reportes.html')

# Vuelve los return JSONs que aceptan tildes
def make_json_response(data, status=200):
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json',
        status=status
    )

# Toda la lógica para reservar citas
@app.route('/citas/reservar_cita', methods=['POST'])
def reservar_cita():
    try:
        data = request.get_json()
        paciente_id = data['paciente_id']
        especialidad = data['especialidad']
        fecha_hora = data['fecha_hora']

        # Valida que el paciente exista
        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            return jsonify({'message': 'Paciente no encontrado'}), 404

        # Filtra los médicos por especialidad
        medicos = Medico.query.filter_by(especialidad=especialidad).all()
        for medico in medicos:
            if isinstance(medico.horarios_disponibles, list):
                horarios_disponibles = [h.strip("'") for h in medico.horarios_disponibles]
            else:
                return jsonify({'message': 'El campo horarios_disponibles tiene un formato inválido'}), 500

            if fecha_hora in horarios_disponibles:
                cita = Cita(
                    fecha=fecha_hora[:9],
                    hora=fecha_hora[11:],
                    estado='Asignada',
                    asistio=None,
                    id_paciente=paciente_id,
                    id_medico=medico.id_medico
                )

                db.session.add(cita)
                db.session.commit()
                return jsonify({'message': 'Cita reservada', 'cita': cita.json()}), 201
            medico.horarios_disponibles.remove(f"'{fecha_hora}'")

        return jsonify({'message': 'No hay médicos disponibles en este horario'}), 400

    except Exception as e:
        return jsonify({'message': 'Error al reservar cita', 'error': str(e)}), 500

# Cancelar citas
@app.route('/citas/cancelar_cita/<int:cita_id>', methods=['PUT'])
def cancelar_cita(cita_id):
    try:
        data = request.get_json()
        asistio = data.get('asistio', False)

        cita = Cita.query.get(cita_id)
        if not cita:
            return jsonify({'message': 'Cita no encontrada'}), 404

        if cita.estado == 'cancelada':
            return jsonify({'message': 'La cita ya está cancelada'}), 409

        cita.estado = 'cancelada'
        cita.asistio = asistio
        db.session.commit()

        return jsonify({'message': 'Cita cancelada', 'cita': cita.json()}), 200
    except Exception as e:
        return jsonify({'message': 'Error al cancelar cita', 'error': str(e)}), 500

# Obtener todas las citas
@app.route('/citas', methods=['GET'])
def get_citas():
    try:
        citas = Cita.query.all()
        return make_json_response({
            'message': 'Citas encontradas',
            'citas': [cita.json() for cita in citas]
        })
    except Exception as e:
        return make_json_response({
            'message': 'Error al buscar las citas',
            'error': str(e)
        }, status=500)

# Ruta para obtener todos los médicos

# Ruta para obtener un solo médico por su ID
@app.route('/medicos/<int:medico_id>', methods=['GET'])
def get_medico(medico_id):
    try:
        medico = Medico.query.filter_by(id_medico=medico_id).first()
        if medico:
            return make_json_response({'Medico': medico.json()})
        else:
            return make_json_response({'message': 'Medico no encontrado'}, status=404)
    except Exception as e:
        return make_json_response({'message': 'Error al traer el médico', 'error': str(e)}, status=500)


@app.route('/crear_medico', methods=['POST'])
def crear_medico():
    try:
        data = request.get_json()
        nuevo_medico = Medico(
            id_medico=data['id_medico'],
            nombre=data['nombre'],
            especialidad=data['especialidad'],
            horarios_disponibles=data['horarios_disponibles']
        )
        db.session.add(nuevo_medico)
        db.session.commit()
        return make_json_response({'message': 'Medico creado'}, status=201)
    except Exception as e:
        return make_json_response({'message': 'Error al crear el médico', 'error': str(e)}, status=500)

# CRUD para Pacientes
@app.route('/pacientes', methods=['GET'])
def get_pacientes():
    try:
        pacientes = Paciente.query.all()
        return make_json_response({
            'message': 'Pacientes encontrados',
            'pacientes': [paciente.json() for paciente in pacientes]
        })
    except Exception as e:
        return make_json_response({'message': 'Error al acceder a los pacientes', 'error': str(e)}, status=500)

@app.route('/pacientes', methods=['POST'])
def crear_paciente():
    try:
        data = request.get_json()
        nuevo_paciente = Paciente(
            id_paciente=data['id_paciente'],
            nombre=data['nombre'],
            telefono=data['telefono'],
            email=data['email'],
            doctor_preferido=data.get('doctor_preferido')
        )
        db.session.add(nuevo_paciente)
        db.session.commit()
        return make_json_response({'message': 'Paciente creado'}, status=201)
    except Exception as e:
        return make_json_response({'message': 'Error al crear el paciente', 'error': str(e)}, status=500)

# Actualizar un paciente
@app.route('/pacientes/<int:id_paciente>', methods=['PUT'])
def actualizar_paciente(id_paciente):
    try:
        data = request.get_json()
        paciente = Paciente.query.get(id_paciente)
        if not paciente:
            return make_json_response({'message': 'Paciente no encontrado'}, status=404)

        paciente.nombre = data.get('nombre', paciente.nombre)
        paciente.telefono = data.get('telefono', paciente.telefono)
        paciente.email = data.get('email', paciente.email)
        paciente.doctor_preferido = data.get('doctor_preferido', paciente.doctor_preferido)

        db.session.commit()

        return make_json_response({'message': 'Paciente actualizado', 'paciente': paciente.json()})
    except Exception as e:
        return make_json_response({'message': 'Error al actualizar el paciente', 'error': str(e)}, status=500)

# Eliminar un paciente
@app.route('/pacientes/<int:id_paciente>', methods=['DELETE'])
def eliminar_paciente(id_paciente):
    try:
        paciente = Paciente.query.get(id_paciente)
        if not paciente:
            return make_json_response({'message': 'Paciente no encontrado'}, status=404)

        db.session.delete(paciente)
        db.session.commit()

        return make_json_response({'message': 'Paciente eliminado'})
    except Exception as e:
        return make_json_response({'message': 'Error al eliminar el paciente', 'error': str(e)}, status=500)

# Exportar reportes a Excel
@app.route('/reporte', methods=['GET'])
def exportar_reporte():
    tipo = request.args.get('tipo')
    if tipo == 'medicos_demandados':
        medicos = Medico.query.all()
        data = [{'medico': m.nombre, 'citas': len(m.citas)} for m in medicos]
    elif tipo == 'motivos_cancelacion':
        citas_canceladas = Cita.query.filter_by(estado='Cancelada').all()
        data = [{'medico': c.id_medico, 'paciente': c.id_paciente, 'fecha': f"{c.fecha}/{c.hora}"} for c in citas_canceladas]
    else:
        return make_json_response({'message': 'Tipo de reporte no válido'}), 400

    df = pd.DataFrame(data)
    output_dir = os.path.join(current_app.instance_path, 'reporte_temp')
    os.makedirs(output_dir, exist_ok=True)
    filename = f'reporte_{tipo}.xlsx'
    filepath = os.path.join(output_dir, filename)
    df.to_excel(filepath, index=False)

    response = send_file(filepath, as_attachment=True, download_name=filename,
                         mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    @response.call_on_close
    def remove_file():
        if os.path.exists(filepath):
            os.remove(filepath)

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
