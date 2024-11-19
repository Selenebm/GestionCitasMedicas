class Medico:
    def __init__(self, nombre: str, id_medico: int, especialidad: str, horarios_disponibles: list):
        self.nombre = nombre
        self.id_medico = id_medico
        self.especialidad = especialidad
        self.horarios_disponibles = horarios_disponibles

    def actualizar_disponibilidad(self, nuevo_horario):
        self.horarios_disponibles = nuevo_horario