

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






// ========================================================================
//                   Evento de clic en el botón de usuario
// ========================================================================
document.getElementById('user-button').addEventListener('click', function(event) {
    var dropdown = document.getElementById('user-dropdown');

    // Verifica si el dropdown está actualmente visible
    if (dropdown.classList.contains('show')) {
        // Si está visible, quita la clase 'show' y añade 'hide' para iniciar la animación de cierre
        dropdown.classList.remove('show');
        dropdown.classList.add('hide');
    } else {
        // Si no está visible, quita la clase 'hide' y añade 'show' para iniciar la animación de apertura
        dropdown.classList.remove('hide');
        dropdown.classList.add('show');
    }

    // Evita que el evento se propague y cierre el dropdown al hacer clic dentro de él
    event.stopPropagation();
});

// Evento de clic en cualquier parte del documento
document.addEventListener('click', function(event) {
    var dropdown = document.getElementById('user-dropdown');
    var button = document.getElementById('user-button');

    // Verifica si el clic no se hizo dentro del dropdown ni del botón
    if (!dropdown.contains(event.target) && !button.contains(event.target)) {
        // Si el dropdown está visible, quita la clase 'show' y añade 'hide' para iniciar la animación de cierre
        if (dropdown.classList.contains('show')) {
            dropdown.classList.remove('show');
            dropdown.classList.add('hide');
        }
    }
});

// Evita que el dropdown se cierre al hacer clic dentro de él
document.getElementById('user-dropdown').addEventListener('click', function(event) {
    event.stopPropagation();
});



// ========================================================================
//                   Evento de Dark Mode
// ========================================================================
document.getElementById('themeToggle').addEventListener('click', function () {
    document.body.classList.toggle('dark-mode');
    // Guarda el estado en localStorage (opcional)
    const isDarkMode = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDarkMode);
});

// Mantén el estado del tema al recargar la página
document.addEventListener('DOMContentLoaded', function () {
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }
});