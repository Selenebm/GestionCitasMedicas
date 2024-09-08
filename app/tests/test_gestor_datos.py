import sys
import os
import unittest
from app.gestor_datos import GestorDeDatos
from app.persona import Paciente  # Ajuste en la ruta de importación
from app.medico import Medico      # Ajuste en la ruta de importación

# Asegurarse de que el directorio correcto esté en el sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestGestorDeDatos(unittest.TestCase):
    def setUp(self):
        self.gestor = GestorDeDatos.get_instancia()
        self.paciente = Paciente("Juan Pérez", 1, "555-555", "juan@example.com")
        self.medico = Medico("Dr. House", 1, "Cardiología", ["10:00", "11:00", "12:00"])

    def test_agregar_paciente(self):
        self.gestor.agregar_paciente(self.paciente)
        self.assertIn(self.paciente, self.gestor.pacientes)

    def test_eliminar_paciente(self):
        self.gestor.agregar_paciente(self.paciente)
        self.gestor.eliminar_paciente(self.paciente)
        self.assertNotIn(self.paciente, self.gestor.pacientes)

    def test_agregar_medico(self):
        self.gestor.agregar_medico(self.medico)
        self.assertIn(self.medico, self.gestor.medicos)

    def test_eliminar_medico(self):
        self.gestor.agregar_medico(self.medico)
        self.gestor.eliminar_medico(self.medico)
        self.assertNotIn(self.medico, self.gestor.medicos)
