from gestor_datos import GestorDeDatos
from persona import Paciente
from medico import Medico  
from agenda import Agenda
from notificacion import Notificacion
from cita import Cita


def main():
    gestor = GestorDeDatos.get_instancia()

    # Crear y agregar médicos
    medico1 = Medico("Dr. House", 1, "Cardiología", ["10:00", "11:00", "12:00"])
    gestor.agregar_medico(medico1)

    # Crear y agregar pacientes
    paciente1 = Paciente("Juan Pérez", 1, "555-555", "juan@example.com", medico1)
    gestor.agregar_paciente(paciente1)

    # Crear cita directamente con el método en Cita
    cita = Cita.crear_cita(medico1, paciente1, "2024-09-15", "10:00")

    # Agendar cita
    agenda = Agenda(1, medico1)
    agenda.agregar_cita(cita)

    # Confirmar cita
    #cita.confirmar_cita()

    # Crear notificación y agregar observadores
    notificacion = Notificacion(1, "Recordatorio", "Recuerde su cita en 2 días.")
    notificacion.suscribir_observador(paciente1)

    # Enviar notificación
    notificacion.enviar_notificacion(cita)

if __name__ == "__main__":
    main()
