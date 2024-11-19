class Notificacion:
    def __init__(self, id_notificacion: int, tipo_notificacion: str, mensaje: str):
        self.id_notificacion = id_notificacion
        self.tipo_notificacion = tipo_notificacion
        self.mensaje = mensaje
        self.observadores = []
