from app.cita import Cita

class FabricaCita:
    def crear_cita(self, medico, paciente, fecha, hora):
        return Cita(None, medico, paciente, fecha, hora, 'Pendiente')