from flask import Flask, render_template, request,redirect, jsonify, url_for, make_response, Response, flash
from models import db, Medico, Paciente, Cita, Notificacion
from datetime import datetime
from __init__ import create_app
import json
import pandas as pd
import os
from flask import send_file, current_app
from werkzeug.utils import secure_filename

app = create_app()

app.secret_key = "secret_key"

# Ruta de prueba
@app.route('/')
def test():
    return render_template("base.html")

#--------------------------------------------
#               Métodos Citas
#--------------------------------------------
# VER Y CREAR CITAS
@app.route('/citas', methods=['GET', 'POST'])
def citas():
    if request.method == "POST":
        try:
            # Obtener datos del formulario
            id_paciente = int(request.form.get('id_paciente'))
            especialidad = request.form.get('especialidad')
            fecha = request.form.get('fecha')
            hora = request.form.get('hora')

            # Validar existencia del paciente
            paciente = Paciente.query.get(id_paciente)
            if not paciente:
                flash("Paciente no encontrado.", "danger")
                return redirect('/citas')

            # Buscar médicos con la especialidad indicada
            medicos = Medico.query.filter_by(especialidad=especialidad).all()
            if not medicos:
                flash("No hay médicos disponibles para esta especialidad.", "danger")
                return redirect('/citas')

            # Asignar al primer médico con disponibilidad en el horario
            for medico in medicos:
                if isinstance(medico.horarios_disponibles, list):
                    horarios_disponibles = [h.strip("'") for h in medico.horarios_disponibles]
                else:
                    flash("Formato inválido en los horarios del médico.", "danger")
                    return redirect('/citas')

                # Verificar si el horario está disponible
                fecha_hora = f"{fecha} {hora}"
                if fecha_hora in horarios_disponibles:
                    # Crear una nueva cita
                    nueva_cita = Cita(
                        fecha=fecha,
                        hora=hora,
                        estado="Asignada",
                        asistio=None,
                        id_paciente=id_paciente,
                        id_medico=medico.id_medico
                    )
                    db.session.add(nueva_cita)

                    # Eliminar el horario de los horarios disponibles del médico
                    horarios_disponibles.remove(fecha_hora)
                    medico.horarios_disponibles = [f"'{h}'" for h in horarios_disponibles]

                    # Guardar los cambios en la base de datos
                    db.session.commit()
                    flash("Cita reservada correctamente.", "success")
                    return redirect('/citas')

            flash("No hay médicos disponibles en este horario.", "danger")
            return redirect('/citas')
        except Exception as e:
            # Manejo de errores
            app.logger.error(f"Error inesperado al reservar cita: {e}")
            db.session.rollback()
            flash("Ocurrió un error al reservar la cita. Inténtalo nuevamente.", "danger")

    # Obtener todas las citas para mostrarlas en la tabla
    citas = Cita.query.all()
    return render_template('citas.html', citas=citas)

#VER CITA EN ESPECIFICO
@app.route('/citas/<int:id_cita>', methods=['GET'])
def get_cita(id_cita):
    cita = Cita.query.filter_by(id_cita=id_cita).first()
    print(cita)
    if cita:
        return render_template("cita.html", cita=cita)
    
    else:
        return render_template("404.html")

#CANCELAR CITAS (SIRVE SOLO POR CONSOLA CON CURL. EN CARPETA DOCS SE ENCUENTRA UN EJEMPLO)
@app.route('/citas/cancelar_cita/<int:cita_id>', methods=['PUT'])
def cancelar_cita(cita_id):
    try:
        data = request.get_json()
        asistio = data.get('asistio', False)  # Asegura un valor por defecto

        # Busca la cita
        cita = Cita.query.get(cita_id)
        if not cita:
            return jsonify({'message': 'Cita no encontrada'}), 404

        if cita.estado == 'cancelada':
            return jsonify({'message': 'La cita ya está cancelada'}), 409

        # Cancela la cita
        cita.estado = 'cancelada'
        cita.asistio = asistio
        db.session.commit()

        return jsonify({'message': 'Cita cancelada', 'cita': cita.json()}), 200
    except Exception as e:
        return jsonify({'message': 'Error al cancelar cita', 'error': str(e)}), 500
    

#--------------------------------------------
#               Métodos Pacientes
#--------------------------------------------  
#VER Y CREAR PACIENTES
@app.route('/pacientes', methods=['GET', 'POST'])
def pacientes():
    if request.method == "POST":
        try:
            id_paciente = int(request.form.get('id_paciente'))
            nombre = request.form.get('nombre')
            telefono = request.form.get('telefono')
            email = request.form.get('email')
            doctor_preferido = int(request.form.get('doctor_preferido'))

            nuevo_paciente = Paciente(
                id_paciente=id_paciente,
                nombre=nombre,
                telefono=telefono,
                email=email,
                doctor_preferido=doctor_preferido
            )

            db.session.add(nuevo_paciente)
            db.session.commit()
            flash("Paciente añadido correctamente.", "success")
        except Exception as e:
            app.logger.error(f"Error inesperado al añadir paciente: {e}")
            db.session.rollback()
            flash("Ocurrió un error. Inténtalo nuevamente.", "danger")

    pacientes = Paciente.query.all()
    return render_template('pacientes.html', pacientes=pacientes)

#VER PACIENTE EN ESPECIFICO
@app.route('/pacientes/<int:id_paciente>', methods=['GET'])
def get_paciente(id_paciente):
    paciente = Paciente.query.filter_by(id_paciente=id_paciente).first()
    if paciente:
        return render_template("paciente.html", paciente=paciente)
    else:
        return render_template("404.html"), 404

# ACTUALIZAR UN PACIENTE (SIRVE SOLO POR CONSOLA CON CURL. EN CARPETA DOCS SE ENCUENTRA UN EJEMPLO)
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

# ELIMINAR UN PACIENTE (SIRVE SOLO POR CONSOLA CON CURL. EN CARPETA DOCS SE ENCUENTRA UN EJEMPLO)
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

#--------------------------------------------
#               Métodos Pacientes
#--------------------------------------------  
#VER Y CREAR MÉDICOS
@app.route('/medicos', methods=['GET', 'POST'])
def medicos():
    if request.method == "POST":
        try:
            # Obtener datos del formulario
            id_medico = int(request.form.get('id_medico'))
            nombre = request.form.get('nombre')
            especialidad = request.form.get('especialidad')
            horarios_disponibles = request.form.get('horarios_disponibles')

            # Crear una nueva instancia de Medico
            nuevo_medico = Medico(
                id_medico=id_medico,
                nombre=nombre,
                especialidad=especialidad,
                horarios_disponibles=horarios_disponibles
            )

            # Agregar y guardar en la base de datos
            db.session.add(nuevo_medico)
            db.session.commit()
            flash("Médico añadido correctamente.", "success")
        except Exception as e:
            # Manejo de errores
            app.logger.error(f"Error inesperado al añadir médico: {e}")
            db.session.rollback()
            flash("Ocurrió un error. Inténtalo nuevamente.", "danger")

    # Obtener la lista de médicos para mostrar en la tabla
    medicos = Medico.query.all()
    return render_template('medicos.html', medicos=medicos)

#RUTA PARA VER UN SOLO MÉDICO
@app.route('/medicos/<int:medico_id>', methods=['GET'])
def get_medico(medico_id):
    medico = Medico.query.filter_by(id_medico=medico_id).first()
    if medico:
        return render_template("medico.html", medico=medico)
    else:
        return render_template("404.html"), 404

#ACTUALIZAR DATOS DE UN MÉDICO (SIRVE SOLO POR CONSOLA CON CURL. EN CARPETA DOCS SE ENCUENTRA UN EJEMPLO)
@app.route('/medicos/<int:medico_id>', methods=['PUT'])
def actualizar_medico(medico_id):
    try:
        data = request.get_json()
        medico = Medico.query.filter_by(id_medico=medico_id).first()
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

#ELIMINAR UN MÉDICO (SIRVE SOLO POR CONSOLA CON CURL. EN CARPETA DOCS SE ENCUENTRA UN EJEMPLO)
@app.route('/medicos/<int:medico_id>', methods=['DELETE'])
def eliminar_medico(medico_id):
    try:
        medico = Medico.query.filter_by(id_medico=medico_id).first()
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


#--------------------------------------------
#               Métodos Pacientes
#--------------------------------------------  
#RUTA PARA MOSTRAR PÁGINA DE LA QUE SE DESCARGAN LOS REPORTES
@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

#PROCESO DE CREACIÓN Y DESCARGA DE LOS REPORTES
@app.route('/reporte', methods=['GET'])
def exportar_reporte():
    tipo = request.args.get('tipo')
    
    if tipo == 'medicos_demandados':
        medicos = Medico.query.all()
        data = [{'medico': m.nombre, 'citas': len(m.citas)} for m in medicos]
    elif tipo == 'motivos_cancelacion':
        citas_canceladas = Cita.query.filter_by(estado='Cancelada').all()
        data = [{'medico': c.id_medico, 'paciente': c.id_paciente,'fecha': f"{c.fecha}/{c.hora}"} for c in citas_canceladas]
    else:
        return make_json_response({'message': 'Tipo de reporte no válido'}), 400

    # Crear DataFrame y archivo en una carpeta temporal
    df = pd.DataFrame(data)
    output_dir = os.path.join(current_app.instance_path, 'reporte_temp')
    os.makedirs(output_dir, exist_ok=True)  # Crea la carpeta si no existe
    filename = f'reporte_{tipo}.xlsx'
    filepath = os.path.join(output_dir, filename)
    df.to_excel(filepath, index=False)

    # Servir el archivo al cliente
    response = send_file(
        filepath,
        as_attachment=True,
        download_name=filename,  # Cambiado de attachment_filename a download_name
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # Eliminar el archivo después de enviarlo
    @response.call_on_close
    def remove_file():
        if os.path.exists(filepath):
            os.remove(filepath)

    return response


# Vuelve los return JSONs que aceptan tildes
def make_json_response(data, status=200):
    return Response(
        json.dumps(data, ensure_ascii=False),
        mimetype='application/json',
        status=status
    )
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
