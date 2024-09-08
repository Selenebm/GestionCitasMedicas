import sys
import os
import unittest
from app.fabrica_cita import FabricaCita
from app.persona import Paciente  
from app.medico import Medico      

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestFabricaCita(unittest.TestCase):
    def setUp(self):
        self.medico = Medico("Dr. House", 1, "Cardiología", ["10:00", "11:00"])
        self.paciente = Paciente("Juan Pérez", 1, "555-555", "juan@example.com")
        self.fabrica_cita = FabricaCita()

    def test_crear_cita(self):
        cita = self.fabrica_cita.crear_cita(self.medico, self.paciente, "2024-09-15", "10:00")
        self.assertEqual(cita.medico, self.medico)
        self.assertEqual(cita.paciente, self.paciente)
        self.assertEqual(cita.fecha, "2024-09-15")
        self.assertEqual(cita.hora, "10:00")
