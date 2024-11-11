from gestor_datos import GestorDeDatos
from medico import Medico  
from agenda import Agenda
from notificacion import Notificacion
from cita import Cita   
from paciente import Paciente

def main():
    gestor = GestorDeDatos.get_instancia()

    # Crear y agregar médicos
    medico1 = Medico("Dr. House", 1, "Cardiología", ["10:00", "11:00", "12:00"])
    medico2 = Medico("Dra. Martínez", 2, "Pediatría", ["14:00", "15:00", "16:00"])
    medico3 = Medico("Dr. López", 3, "Dermatología", ["10:00", "11:30", "13:00"])
    medico4 = Medico("Dra. Gómez", 4, "Neurología", ["08:00", "09:00", "10:30"])
    medico5 = Medico("Dr. Ramírez", 5, "Ginecología", ["13:00", "14:30", "16:00"])
    medico6 = Medico("Dra. Sánchez", 6, "Cardiología", ["12:00", "13:00", "14:00"])
    medico7 = Medico("Dr. Fernández", 7, "Psiquiatría", ["09:30", "11:00", "12:30"])
    medico8 = Medico("Dra. Rivera", 8, "Oncología", ["10:00", "11:00", "12:00"])
    medico9 = Medico("Dr. Torres", 9, "Oftalmología", ["15:00", "16:00", "17:00"])
    medico10 = Medico("Dra. Delgado", 10, "Endocrinología", ["09:00", "10:30", "12:00"])

    # Agregar médicos al gestor de datos
    gestor.agregar_medico(medico1)
    gestor.agregar_medico(medico2)
    gestor.agregar_medico(medico3)
    gestor.agregar_medico(medico4)
    gestor.agregar_medico(medico5)
    gestor.agregar_medico(medico6)
    gestor.agregar_medico(medico7)
    gestor.agregar_medico(medico8)
    gestor.agregar_medico(medico9)
    gestor.agregar_medico(medico10)

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
