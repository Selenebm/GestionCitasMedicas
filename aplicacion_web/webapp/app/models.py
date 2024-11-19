from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Medico(db.Model):
    __tablename__ = 'Medicos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    # Almacenar horarios como un array de texto
    horarios_disponibles = db.Column(db.ARRAY(db.Text), nullable=False, default=[])
    citas = db.relationship('Cita', backref='medico', lazy=True)
    
    def __repr__(self):
        return f'<Medico {self.nombre}>'

class Paciente(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    doctor_preferido = db.relationship('Medico', backref='pacientes', lazy=True)
    citas = db.relationship('Cita', backref='paciente', lazy=True)

    def __repr__(self):
        return f'<Paciente {self.nombre}>'
    
class Cita(db.Model):
    __tablename__ = 'citas'
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    hora = db.Column(db.Time, nullable=False)
    estado = db.Column(db.String(20), nullable=False, default='pendiente')
    motivo_cancelacion = db.Column(db.Text)
    medico_id = db.Column(db.Integer, db.ForeignKey('medicos.id'))
    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'))

    def __repr__(self):
        return f'<Cita {self.id}>'
    
class Notificacion(db.Model):
    __tablename__ = 'notificaciones'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    mensaje = db.Column(db.Text, nullable=False)
    cita_id = db.Column(db.Integer, db.ForeignKey('citas.id'))

    def __repr__(self):
        return f'<Notificacion {self.id}>'