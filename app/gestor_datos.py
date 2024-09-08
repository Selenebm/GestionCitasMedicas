# gestor_datos.py
from app.persona import Paciente
from app.medico import Medico  # Corrige esta importación

class GestorDeDatos:
    _instancia = None

    def __init__(self):
        if GestorDeDatos._instancia is not None:
            raise Exception("Esta clase es un Singleton. Usa 'get_instancia()'.")
        self.pacientes = []
        self.medicos = []

    @staticmethod
    def get_instancia():
        if GestorDeDatos._instancia is None:
            GestorDeDatos._instancia = GestorDeDatos()
        return GestorDeDatos._instancia

    def agregar_paciente(self, paciente: Paciente):
        self.pacientes.append(paciente)

    def eliminar_paciente(self, paciente: Paciente):
        self.pacientes.remove(paciente)

    def buscar_paciente_por_id(self, id_paciente: int):
        for paciente in self.pacientes:
            if paciente.id_paciente == id_paciente:
                return paciente
        return None

    def agregar_medico(self, medico: Medico):
        self.medicos.append(medico)

    def eliminar_medico(self, medico: Medico):
        self.medicos.remove(medico)

    def buscar_medico_por_id(self, id_medico: int):
        for medico in self.medicos:
            if medico.id_medico == id_medico:
                return medico
        return None
