# **Gestión de citas médicas - Requerimientos -> Selene Belalcázar Muñoz**

## **El sistema antiguo cuenta con lo siguiente, pero el sistema actual también debe de:** 

- Los pacientes llaman para agendar citas.
- Se verifica la disponibilidad de los médicos según su especialidad.
- Algunos pacientes ya tienen un médico asignado o seleccionado.
- Se ofrece la cita al paciente según los cupos, además el paciente elige que día y se registra en una agenda física.
- Dos días antes, se llama al paciente para confirmar la cita recordando el día y la hora.

## **Problemas identificados que presentaba el sistema antiguo para tomar encuenta en el actual:** 

- Dificultad para manejar la disponibilidad de los médicos con agendas físicas.
- Problemas para actualizar los cambios en la disponibilidad de los médicos.
- Cancelación de citas manual que requiere contacto telefónico con otros pacientes.


## **Requerimientos, el sistema debe de:**

- Tener un manejo de la agenda de los médicos.
- Permitir a los pacientes registrados agendar sus citas en línea, mostrando la disponibilidad en tiempo real.
- Enviar confirmaciones de citas por correo electrónico, SMS o notificación móvil.
- Recordatorio dos días antes de la cita.
- Los pacientes deben poder cancelar sus citas y liberar los horarios automáticamente.
- Ser capaz de integrarse con otros medios de contacto (como Whatsapp o Slack) si se decide utilizarlos en el futuro. ---> *Dejar integrado para el futuro*
- Permitir almacenar la información de los pacientes y médicos de forma digital.
- Generar informe y reportes de lo siguiente: 
		
			+ Reportes sobre los médicos más solicitados y su especialidad.
			+ Análisis de la tendencia de citas y ausencias.
			+ Identificación de causas de cancelación.
			+ Evaluar la eficiencia de las consultas.
			+ Posibilidad de exportar los reportes a Excel.
