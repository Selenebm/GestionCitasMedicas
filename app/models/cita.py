from database import db

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