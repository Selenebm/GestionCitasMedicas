class Paciente:
    def __init__(self, nombre: str, id_paciente: int, telefono: str, email: str, doctor_preferido=None):
        self.nombre = nombre
        self.id_paciente = id_paciente
        self.telefono = telefono
        self.email = email
        self.doctor_preferido = doctor_preferido

    def actualizar_contacto(self, nuevo_telefono: str, nuevo_email: str):
        self.telefono = nuevo_telefono
        self.email = nuevo_email
        print(f"Contacto actualizado para {self.nombre}. Teléfono: {self.telefono}, Email: {self.email}")

    def actualizar_cita(self, cita):
        print(f"Paciente {self.nombre} ha sido notificado sobre la cita: {cita.id_cita} el {cita.fecha} a las {cita.hora}.")

    def confirmar_cita(self, cita):
        cita.estado = 'Confirmada'
        print(f"Cita {cita.id_cita} confirmada para el paciente {self.nombre}")

    def cancelar_cita(self, cita):
        cita.estado = 'Cancelada'
        print(f"Cita {cita.id_cita} cancelada para el paciente {self.nombre}")

