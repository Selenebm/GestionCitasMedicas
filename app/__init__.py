from flask import Flask
from .models import db
from . import routes
from .config import Config


# def __init__(self, id_cita: int, medico, paciente, fecha: str, hora: str, estado: str):
#     self.id_cita = id_cita
#     self.medico = medico
#     self.paciente = paciente
#     self.fecha = fecha
#     self.hora = hora
#     self.estado = estado
#     self.asistio = False
