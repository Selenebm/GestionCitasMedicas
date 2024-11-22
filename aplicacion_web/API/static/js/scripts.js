// Función para editar un paciente
function editarPaciente(id) {
    fetch(`/pacientes/${id}`)
        .then(response => response.json())
        .then(data => {
            // Llena el formulario con los datos del paciente
            document.getElementById('nombre').value = data.nombre;
            document.getElementById('telefono').value = data.telefono;
            document.getElementById('email').value = data.email;
            document.getElementById('doctor_preferido').value = data.doctor_preferido;

            // Guarda el ID en el formulario
            document.getElementById('form-paciente').dataset.id = id;
        })
        .catch(error => console.error('Error al obtener paciente:', error));
}

// Función para eliminar un paciente
function eliminarPaciente(id) {
    if (confirm('¿Seguro que deseas eliminar este paciente?')) {
        fetch(`/pacientes/${id}`, {
            method: 'DELETE',
        })
            .then(response => response.json())
            .then(result => {
                alert(result.message);
                location.reload(); // Recarga la página para actualizar la lista
            })
            .catch(error => console.error('Error al eliminar paciente:', error));
    }
}

