from cita import Cita

class Agenda:
    def __init__(self, id_agenda: int, medico):
        self.id_agenda = id_agenda
        self.medico = medico
        self.citas = []

    def agregar_cita(self, cita: Cita):
        # Verificar si el horario de la cita está disponible
        if cita.hora not in self.medico.horarios_disponibles:
            raise ValueError(f"El horario {cita.hora} no está disponible para el médico {self.medico.nombre}.")

        # Agregar cita a la agenda si el horario está disponible
        self.citas.append(cita)
        self.actualizar_disponibilidad(cita.hora)

    def eliminar_cita(self, cita: Cita):
        self.citas.remove(cita)

    def consultar_disponibilidad(self):
        # Devuelve los horarios disponibles del médico
        return self.medico.horarios_disponibles

    def actualizar_disponibilidad(self, hora: str):
        # Actualiza la lista de horarios disponibles eliminando el horario agendado
        if hora in self.medico.horarios_disponibles:
            self.medico.horarios_disponibles.remove(hora)

