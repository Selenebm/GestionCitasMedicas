import sys
import os
import unittest
from app.medico import Medico
from app.cita import Cita

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestMedico(unittest.TestCase):
    def setUp(self):
        self.medico = Medico("Dr. House", 1, "Cardiología", ["10:00", "11:00"])
        self.cita_test = Cita(1, self.medico, "Paciente Test", "2024-09-15", "10:00", 'Pendiente')

    def test_actualizar_disponibilidad(self):
        self.medico.actualizar_disponibilidad(["09:00", "13:00"])
        self.assertEqual(self.medico.horarios_disponibles, ["09:00", "13:00"])

    def test_actualizar_cita(self):
        self.medico.actualizar_cita(self.cita_test)
        # No debería lanzar ninguna excepción.