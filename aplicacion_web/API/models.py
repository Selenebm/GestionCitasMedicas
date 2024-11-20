from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Medico(db.Model):
    __tablename__ = 'medicos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    horarios_disponibles = db.Column(db.ARRAY(db.String), nullable=False)  # List of available times
    citas = db.relationship('Cita', back_populates='medico')

    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'especialidad': self.especialidad,
            'horarios_disponibles': self.horarios_disponibles
        }

class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    doctor_preferido_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=True)
    doctor_preferido = db.relationship('Medico')
    citas = db.relationship('Cita', back_populates='paciente')

    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'telefono': self.telefono,
            'email': self.email,
            'doctor_preferido_id': self.doctor_preferido_id
        }

class Cita(db.Model):
    __tablename__ = 'citas'

    id = db.Column(db.Integer, primary_key=True)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    motivo = db.Column(db.String(255), nullable=True)  # Reason for cancellation
    estado = db.Column(db.String(50), default='programada')  # 'programada', 'cancelada', 'completada'
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)

    paciente = db.relationship('Paciente', back_populates='citas')
    medico = db.relationship('Medico', back_populates='citas')

    def json(self):
        return {
            'id': self.id,
            'fecha_hora': self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S'),
            'estado': self.estado,
            'motivo': self.motivo,
            'paciente_id': self.paciente_id,
            'medico_id': self.medico_id
        }

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'

    id = db.Column(db.Integer, primary_key=True)
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'), nullable=False)
    mensaje = db.Column(db.String(255), nullable=False)
    enviado = db.Column(db.Boolean, default=False)

    cita = db.relationship('Cita')

    def json(self):
        return {
            'id': self.id,
            'cita_id': self.cita_id,
            'mensaje': self.mensaje,
            'enviado': self.enviado
        }
