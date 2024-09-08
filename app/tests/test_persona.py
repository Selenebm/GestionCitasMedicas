import sys
import os
import unittest
from app.persona import Persona, Paciente
from app.cita import Cita

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestPersona(unittest.TestCase):
    def setUp(self):
        self.persona = Persona("Juan Pérez", "555-555", "juan@example.com")

    def test_actualizar_contacto(self):
        self.persona.actualizar_contacto("999-999", "nuevo@example.com")
        self.assertEqual(self.persona.telefono, "999-999")
        self.assertEqual(self.persona.email, "nuevo@example.com")

class TestPaciente(unittest.TestCase):
    def setUp(self):
        self.paciente = Paciente("Juan Pérez", 1, "555-555", "juan@example.com")
        self.cita_test = Cita(1, "Medico Test", self.paciente, "2024-09-15", "10:00", 'Pendiente')

    def test_actualizar_cita(self):
        self.paciente.actualizar_cita(self.cita_test)
        # No debería lanzar ninguna excepción.