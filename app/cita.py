class Cita:
    def __init__(self, id_cita: int, medico, paciente, fecha: str, hora: str, estado: str):
        self.id_cita = id_cita
        self.medico = medico
        self.paciente = paciente
        self.fecha = fecha
        self.hora = hora
        self.estado = estado
        self.asistio = False

    @staticmethod
    def crear_cita(medico, paciente, fecha, hora):
        # Método adicional para crear una cita
        return Cita(None, medico, paciente, fecha, hora, 'Pendiente')

