from observador import Observador

class Notificacion:
    def __init__(self, id_notificacion: int, tipo_notificacion: str, mensaje: str):
        self.id_notificacion = id_notificacion
        self.tipo_notificacion = tipo_notificacion
        self.mensaje = mensaje
        self.observadores = []

    def suscribir_observador(self, observador: Observador):
        self.observadores.append(observador)

    def desuscribir_observador(self, observador: Observador):
        self.observadores.remove(observador)

    def enviar_notificacion(self, cita):
        for observador in self.observadores:
            observador.actualizar_cita(cita)
