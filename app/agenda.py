from cita import Cita
from fabrica_cita import FabricaCita

class Agenda:
    def __init__(self, id_agenda: int, medico):
        self.id_agenda = id_agenda
        self.medico = medico
        self.citas = []

    def agregar_cita(self, cita: Cita):
        self.citas.append(cita)

    def eliminar_cita(self, cita: Cita):
        self.citas.remove(cita)

    def consultar_disponibilidad(self):
        return self.medico.horarios_disponibles

    def fabricar_cita(self, medico, paciente, fecha, hora):
        fabrica = FabricaCita()
        return fabrica.crear_cita(medico, paciente, fecha, hora)
