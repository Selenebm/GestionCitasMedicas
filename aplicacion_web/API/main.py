from models import db, Medico, Paciente, Cita, Notificacion
from datetime import datetime
from __init__ import create_app
from flask import Response, make_response, jsonify, request
import json
import pandas as pd

app = create_app()


@app.route('/')
def test():
    return make_response(jsonify({'message': 'test route'}), 200)

# Vuelve los return JSONs que aceptan tildes
def make_json_response(data, status=200):
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json',
        status=status
    )

# Toda la logica para reservar citas
@app.route('/reservar_cita', methods=['POST'])
def reservar_cita():
    data = request.get_json()
    paciente_id = data['paciente_id']
    especialidad = data['especialidad']
    fecha_hora = datetime.strptime(data['fecha_hora'], '%Y-%m-%d %H:%M:%S')

    # Valida que el paciente exista
    paciente = Paciente.query.get(paciente_id)
    if not paciente:
        return jsonify({'message': 'Paciente no encontrado'})

    # filtra el doctor por especialidad
    medicos = Medico.query.filter_by(especialidad=especialidad).all()
    for medico in medicos:
        if fecha_hora.strftime('%H:%M') in medico.horarios_disponibles:
            # verifica que no se choquen los horarios
            if not any(c.fecha_hora == fecha_hora for c in medico.citas):
                # Agenda la cita
                cita = Cita(
                    fecha_hora=fecha_hora,
                    paciente_id=paciente_id,
                    medico_id=medico.id
                )
                db.session.add(cita)
                db.session.commit()
                return jsonify({'message': 'Cita reservada', 'cita': cita.json()})

    return jsonify({'message': 'No hay médicos disponibles en este horario'})

# Para cancelar citas
@app.route('/cancelar_cita/<int:cita_id>', methods=['PUT'])
def cancelar_cita(cita_id):
    data = request.get_json()
    motivo = data.get('motivo')

    cita = Cita.query.get(cita_id)
    if not cita:
        return jsonify({'message': 'Cita no encontrada'})

    if cita.estado == 'cancelada':
        return jsonify({'message': 'La cita ya está cancelada'})

    cita.estado = 'cancelada'
    cita.motivo = motivo
    db.session.commit()

    return jsonify({'message': 'Cita cancelada', 'cita': cita.json()})

# --------------------------------------------
# CRUD Medicos
# --------------------------------------------

# Muestra todos los medicos
@app.route('/medicos', methods=['GET'])
def get_medicos():
    try:
        medicos = Medico.query.all()
        return make_json_response({
            'message': 'Medicos encontrados',
            'medicos': [medico.json() for medico in medicos]
        })
    except Exception as e:
        return make_json_response({
            'message': 'Error al acceder a la base de datos',
            'error': str(e)
        }, status=500)
    
# Muestra medico por id
@app.route('/medicos/<int:medico_id>', methods=['GET'])
def get_medico(medico_id):
    try:
        medico = Medico.query.filter_by(medico_id=medico_id).first()
        if medico:
            return make_json_response({'Medico': medico.json()})
        else:
            return make_json_response({'message': 'Medico no encontrado'}, status=404)
    except Exception as e:
        return make_json_response({
            'message': 'Error al traer el médico',
            'error': str(e)
        }, status=500)

@app.route('/crear_medico', methods=['POST'])
def crear_medico():
    try:
        data = request.get_json()
        nuevo_medico = Medico(
            nombre=data['nombre'],
            especialidad=data['especialidad'],
            horarios_disponibles=data['horarios_disponibles']
        )
        db.session.add(nuevo_medico)
        db.session.commit()
        return make_json_response({'message': 'Medico creado'}, status=201)
    except Exception as e:
        return make_json_response({
            'message': 'Error al crear el médico',
            'error': str(e)
        }, status=500)


@app.route('/medicos/<int:medico_id>', methods=['PUT'])
def actualizar_medico(medico_id):
    try:
        data = request.get_json()
        medico = Medico.query.filter_by(medico_id=medico_id).first()
        if medico:
            medico.nombre = data['nombre']
            medico.especialidad = data['especialidad']
            medico.horarios_disponibles = data['horarios_disponibles']
            db.session.commit()
            return make_json_response({'message': 'Medico actualizado'})
        else:
            return make_json_response({'message': 'Medico no encontrado'}, status=404)
    except Exception as e:
        return make_json_response({
            'message': 'Error al actualizar el médico',
            'error': str(e)
        }, status=500)


@app.route('/medicos/<int:medico_id>', methods=['DELETE'])
def eliminar_medico(medico_id):
    try:
        medico = Medico.query.filter_by(medico_id=medico_id).first()
        if medico:
            db.session.delete(medico)
            db.session.commit()
            return make_json_response({'message': 'Medico eliminado'})
        else:
            return make_json_response({'message': 'Medico no encontrado'}, status=404)
    except Exception as e:
        return make_json_response({
            'message': 'Error al eliminar el médico',
            'error': str(e)
        }, status=500)


# --------------------------------------------
# CRUD Pacientes
# --------------------------------------------

@app.route('/pacientes', methods=['GET'])
def get_pacientes():
    try:
        pacientes = Paciente.query.all()
        return make_json_response({
            'message': 'Pacientes encontrados',
            'pacientes': [paciente.json() for paciente in pacientes]
        })
    except Exception as e:
        return make_json_response({
            'message': 'Error al acceder a los pacientes',
            'error': str(e)
        }, status=500)


@app.route('/pacientes', methods=['POST'])
def crear_paciente():
    try:
        data = request.get_json()
        nuevo_paciente = Paciente(
            nombre=data['nombre'],
            telefono=data['telefono'],
            email=data['email'],
            doctor_preferido=data.get('doctor_preferido')  # Optional
        )
        db.session.add(nuevo_paciente)
        db.session.commit()
        return make_json_response({'message': 'Paciente creado'}, status=201)
    except Exception as e:
        return make_json_response({
            'message': 'Error al crear el paciente',
            'error': str(e)
        }, status=500)


@app.route('/pacientes/<int:paciente_id>', methods=['GET'])
def get_paciente(paciente_id):
    try:
        paciente = Paciente.query.get_or_404(paciente_id)
        return make_json_response({'Paciente': paciente.json()})
    except Exception as e:
        return make_json_response({
            'message': 'Error al traer el paciente',
            'error': str(e)
        }, status=500)


@app.route('/pacientes/<int:paciente_id>', methods=['PUT'])
def actualizar_paciente(paciente_id):
    try:
        data = request.get_json()
        paciente = Paciente.query.get_or_404(paciente_id)
        paciente.nombre = data['nombre']
        paciente.telefono = data['telefono']
        paciente.email = data['email']
        paciente.doctor_preferido = data.get('doctor_preferido')  # Optional
        db.session.commit()
        return make_json_response({'message': 'Paciente actualizado'})
    except Exception as e:
        return make_json_response({
            'message': 'Error al actualizar el paciente',
            'error': str(e)
        }, status=500)


@app.route('/pacientes/<int:paciente_id>', methods=['DELETE'])
def eliminar_paciente(paciente_id):
    try:
        paciente = Paciente.query.get_or_404(paciente_id)
        db.session.delete(paciente)
        db.session.commit()
        return make_json_response({'message': 'Paciente eliminado'})
    except Exception as e:
        return make_json_response({
            'message': 'Error al eliminar el paciente',
            'error': str(e)
        }, status=500)


# Exportar reportes a excel
@app.route('/reporte', methods=['GET'])
def exportar_reporte():
    tipo = request.args.get('tipo')
    if tipo == 'medicos_demandados':
        medicos = Medico.query.all()
        data = [{'medico': m.nombre, 'citas': len(m.citas)} for m in medicos]
    elif tipo == 'motivos_cancelacion':
        citas_canceladas = Cita.query.filter_by(estado='cancelada').all()
        data = [{'motivo': c.motivo, 'fecha': c.fecha_hora} for c in citas_canceladas]
    else:
        return jsonify({'message': 'Tipo de reporte no válido'}), 400

    # Create DataFrame
    df = pd.DataFrame(data)
    filename = f'reporte_{tipo}.xlsx'
    df.to_excel(filename, index=False)

    return jsonify({'message': 'Reporte exportado', 'file': filename}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
