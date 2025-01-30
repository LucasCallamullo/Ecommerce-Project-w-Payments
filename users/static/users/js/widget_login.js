

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
        dropdown.style.display = 'block';
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

document.getElementById('user-dropdown').addEventListener('animationend', function(event) {
    var dropdown = document.getElementById('user-dropdown');
    
    // Verifica si la animación que terminó fue 'slideUp'
    if (event.animationName === 'slideUp') {
        dropdown.style.display = 'none'; // Oculta el dropdown después de la animación
    }
});


// ========================================================================
//           Validación generica de formularios con alertas de user
// ========================================================================
function validFormsWithAlerts(form) {
    form.addEventListener('submit', async function(event) {
        // Evita que el formulario se envíe de forma tradicional
        event.preventDefault(); 
        
        const formData = new FormData(form);

        try {
            // mandamomos como url la action del formulario
            const response = await fetch(form.action, { 
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest' 
                }
            });

            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor.');
            }

            const data = await response.json(); // Procesar la respuesta como JSON

            if (data.success) {
                // La funcion openAlert viene de home/js/base.js
                openAlert('Registro exitoso', 'green', 1000);
                
                // verificar bien despues el comportamiento de redirigir
                setTimeout(() => {
                    window.location.href = data.redirect_url; 
                }, 1000);

            } else {
                // La funcion openAlert viene de home/js/base.js
                const message = data.error || 'Ocurrió un error inesperado.';
                openAlert(message, 'red', 2000);
            }
        } catch (error) {
            console.error('Error:', error);
            openAlert('Error al procesar la solicitud. Intenta nuevamente.', 'red', 2000);
        }
    });
}

// ========================================================================
//           Validación generica de formularios con alertas de user
// ========================================================================
function loginUser(form, widget = true) {
    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Evitamos el envío del formulario por defecto

        // Identificar los campos de email y contraseña según el formulario
        let emailID = widget ? "w-email" : "email";
        let passID = widget ? "w-password" : "password";
        let emailInput = document.getElementById(emailID);
        let passInput = document.getElementById(passID);

        const formData = {
            email: emailInput ? emailInput.value : "",
            password: passInput ? passInput.value : "",
        };

        try {
            // Mandamos los datos como POST al servidor usando la URL del formulario
            const response = await fetch(form.action, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(formData), // Convierte los datos del formulario a JSON
                credentials: "include", // IMPORTANTE si usas cookies para autenticación
            });

            if (!response.ok) {
                throw new Error("Error en la respuesta del servidor.");
            }

            const data = await response.json(); // Procesa la respuesta como JSON

            if (data.tokens) {
                
                // También guardar en cookies (pero idealmente debería hacerse en el backend)
                // document.cookie = `access_token=${data.tokens.access}; path=/; HttpOnly=true`;

                openAlert("Login exitoso!", "green", 1000);

                // Redirigir a otra página después de un breve delay
                setTimeout(() => {
                    window.location.href = data.redirect_url;
                }, 1000);

            } else {
                openAlert("Error: " + (data.detail || "No se recibieron tokens"), "red", 2000);
            }
        } catch (error) {
            console.error("Error:", error);
            openAlert("Error al procesar la solicitud. Intenta nuevamente.", "red", 2000);
        }
    });
}


// Capturamos el evento del envío de datos al formulario
document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('widget-register-form');
    if (form) {
        loginUser(form);
    } else {
        console.error("Formulario no encontrado.");
    }
});




// Esta funcion es para cambiar lo que se muestra una vez que esta logeado
document.addEventListener('DOMContentLoaded', function() {
    
    const user_span = document.getElementById('user-email')
    const datasos = user_span.dataset;

    const email = datasos.email || '0';
    const name = datasos.name || '0';
    const lastName = datasos.lastName || '0';

    if (name !== '0') {
        var username = name + ' ' + lastName
    } else {
        // Obtener la parte antes del '@'
        var username = email.split('@')[0];
    }

    user_span.textContent = username;
});
