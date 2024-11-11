from observador import Observador

class Persona:
    def __init__(self, nombre: str, telefono: str, email: str):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def actualizar_contacto(self, nuevo_telefono: str, nuevo_email: str):
        self.telefono = nuevo_telefono
        self.email = nuevo_email

class Paciente(Persona, Observador):
    def __init__(self, nombre: str, id_paciente: int, telefono: str, email: str, doctor_preferido=None):
        super().__init__(nombre, telefono, email)
        self.id_paciente = id_paciente
        self.doctor_preferido = doctor_preferido

    def agendar_cita(self, cita):
        pass

    def cancelar_cita(self, cita):
        pass

    def actualizar_cita(self, cita):
        print(f"Paciente {self.nombre} ha sido notificado sobre la cita: {cita.id_cita} el {cita.fecha} a las {cita.hora}.")
