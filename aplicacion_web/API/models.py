from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Medico(db.Model):
    __tablename__ = 'medicos'

    id_medico = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    horarios_disponibles = db.Column(db.ARRAY(db.String), nullable=False)  # List of available times
    citas = db.relationship('Cita', back_populates='medico')

    def json(self):
        return {
            'id': self.id_medico,
            'nombre': self.nombre,
            'especialidad': self.especialidad,
            'horarios_disponibles': self.horarios_disponibles
        }

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id_paciente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    doctor_preferido = db.Column(db.Integer, db.ForeignKey('medicos.id_medico'), nullable=True)
    #doctor_preferido = db.relationship('Medico')
    citas = db.relationship('Cita', back_populates='paciente')

    def json(self):
        return {
            'id': self.id_paciente,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email,
            'doctor_preferido_id': self.doctor_preferido
        }

class Cita(db.Model):
    __tablename__ = 'citas'

    id_cita = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    hora = db.Column(db.Time, nullable = False)
    estado = db.Column(db.String(50), default='Asignada')  # 'Asignada', 'Cancelada', 'Movida'
    asistio = db.Column(db.Boolean, nullable=True)  
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id_paciente'), nullable=False)
    id_medico = db.Column(db.Integer, db.ForeignKey('medicos.id_medico'), nullable=False)

    paciente = db.relationship('Paciente', back_populates='citas')
    medico = db.relationship('Medico', back_populates='citas')

    def json(self):
        return {
            'id': self.id_cita,
            'fecha': self.fecha.strftime('%Y-%m-%d'),
            'hora': self.hora.strftime('%H:%M'),
            'estado': self.estado,
            'asisitio': self.asistio,
            'paciente_id': self.id_paciente,
            'medico_id': self.id_medico
        }

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'

    id_notificacion = db.Column(db.Integer, primary_key=True)
    id_cita = db.Column(db.Integer, db.ForeignKey('citas.id_cita'), nullable=False)
    fecha_envio = db.Column(db.DateTime)
    tipo_notificacion = db.Column(db.String(50))
    mensaje = db.Column(db.String(255), nullable=False)

    cita = db.relationship('Cita')

    def json(self):
        return {
            'id': self.id_notificacion,
            'cita_id': self.id_cita,
            'mensaje': self.mensaje,
            'enviado': self.enviado
        }
