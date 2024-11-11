class Cita:
    _id_counter = 1  # Contador para IDs únicos

    def __init__(self, id_cita: int, medico, paciente, fecha: str, hora: str, estado: str):
        self.id_cita = id_cita
        self.medico = medico
        self.paciente = paciente
        self.fecha = fecha
        self.hora = hora
        self.estado = estado
        self.asistio = False

    @classmethod
    def crear_cita(cls, medico, paciente, fecha, hora):
        # Asigna automáticamente un id_cita usando el contador de clase
        cita = cls(cls._id_counter, medico, paciente, fecha, hora, 'Pendiente')
        cls._id_counter += 1  # Incrementa el contador para el siguiente id
        return cita


