

// ========================================================================
//                   Evento de anmimaciones en drop menu categories
// ========================================================================
// Evento de clic en el botón de usuario
document.getElementById('navbarDropdown').addEventListener('click', function(event) {
    var dropdown_cat = document.getElementById('categories-drop');
    var arrow_drop = document.querySelector('.arrow-drop');

    // Verifica si el dropdown está actualmente visible
    if (dropdown_cat.classList.contains('show')) {
        // Si está visible, quita la clase 'show' y añade 'hide' para iniciar la animación de cierre
        dropdown_cat.classList.remove('show');
        dropdown_cat.classList.add('hide');
    } else {
        // Si no está visible, quita la clase 'hide' y añade 'show' para iniciar la animación de apertura
        dropdown_cat.classList.remove('hide');
        dropdown_cat.classList.add('show');
    }

    arrow_drop.classList.toggle('rotate');

    // Evita que el evento se propague y cierre el dropdown al hacer clic dentro de él
    event.stopPropagation();
});

// Evento de clic en cualquier parte del documento
document.addEventListener('click', function(event) {
    var dropdown_cat = document.getElementById('categories-drop');
    var button_cat = document.getElementById('navbarDropdown');
    var arrow_drop = document.querySelector('.arrow-drop');

    // Verifica si el clic no se hizo dentro del dropdown ni del botón
    if (!dropdown_cat.contains(event.target) && !button_cat.contains(event.target)) {
        // Si el dropdown está visible, quita la clase 'show' y añade 'hide' para iniciar la animación de cierre
        if (dropdown_cat.classList.contains('show')) {
            dropdown_cat.classList.remove('show');
            dropdown_cat.classList.add('hide');
            arrow_drop.classList.toggle('rotate');
        }
    }
});

// Evita que el dropdown se cierre al hacer clic dentro de él
document.getElementById('categories-drop').addEventListener('click', function(event) {
    event.stopPropagation();
});


/* ==========================================================================================
              Función Generica para Eventos de mostrar y ocultar alertas
========================================================================================== */
function openAlert(message, color='', timeout=1000) {
    const alertsContainer = document.getElementById('alertsContainer');
    
    // Crear una nueva alerta
    const alertBox = document.createElement('div');
    alertBox.classList.add('custom-alert');
    
    // Establecer el ícono según el color
    const icon = document.createElement('i');
    if (color === 'red') {
        icon.classList.add('fa-regular', 'fa-circle-xmark');
    } else {
        icon.classList.add('fa-regular', 'fa-circle-check');
    }
    alertBox.appendChild(icon);


    // Establecer el mensaje
    const alertMessage = document.createElement('span');
    alertMessage.classList.add('alert-message');
    alertMessage.textContent = message;
    alertBox.appendChild(alertMessage);

    // Agregar el botón de cierre
    const closeButton = document.createElement('button');
    closeButton.innerHTML = '<i class="fa-solid fa-xmark"></i>';
    closeButton.onclick = function() {
        closeAlert(alertBox);
    };
    alertBox.appendChild(closeButton);

    // Agregar la clase correspondiente para el color
    if (color === 'red') {
        alertBox.classList.add('alert-red');
    } else {
        alertBox.classList.add('alert-green');
    }

    // Insertar la nueva alerta en el contenedor
    // alertsContainer.appendChild(alertBox);

    // Insertar la nueva alerta en el contenedor en la primera posición 
    alertsContainer.insertBefore(alertBox, alertsContainer.firstChild);

    // Mostrar la alerta con animación
    setTimeout(() => {
        alertBox.classList.add('show');
    }, 10); // Asegura que la clase se aplique después de que se haya añadido al DOM

    // Cerrar la alerta después del tiempo especificado
    setTimeout(() => {
        closeAlert(alertBox);
    }, timeout);
}

function closeAlert(alertBox) {
    alertBox.classList.remove('show');
    alertBox.classList.add('hidden');
    // Eliminar la alerta después de la animación de ocultado
    setTimeout(() => {
        alertBox.remove();
    }, 400); // Asegura que se elimine después de la animación
}



// ========================================================================
//                   Evento de Dark Mode
// ========================================================================
const themeToggleButton = document.getElementById('themeToggle');
const themeIcon = document.getElementById('theme-icon');

// Función para alternar el modo oscuro y actualizar el ícono
function toggleTheme() {
    const isDarkMode = document.body.classList.toggle('dark-mode'); // Cambia el modo
    themeIcon.classList.toggle('fa-moon', !isDarkMode); // Muestra el sol para modo luz
    themeIcon.classList.toggle('fa-sun', isDarkMode); // Muestra la luna para modo oscuro

    // Guarda el estado en localStorage
    localStorage.setItem('darkMode', isDarkMode);
}

// Asigna el evento al botón
themeToggleButton.addEventListener('click', toggleTheme);

// Mantén el estado del tema y el ícono al recargar la página
document.addEventListener('DOMContentLoaded', function () {
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        themeIcon.classList.add('fa-sun');
        themeIcon.classList.remove('fa-moon');
    } else {
        themeIcon.classList.add('fa-moon');
        themeIcon.classList.remove('fa-sun');
    }
});