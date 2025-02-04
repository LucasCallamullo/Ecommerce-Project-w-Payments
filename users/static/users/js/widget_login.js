

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
async function handleFormActions(form, actionType) {
    form.addEventListener("submit", async function (event) {
        event.preventDefault(); // Evitar el envío del formulario por defecto

        // Convertimos FormData en JSON
        const formData = new FormData(form);
        const jsonData = Object.fromEntries(formData.entries());

        try {
            const response = await fetch(form.action, {
                method: "POST",
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    "Content-Type": "application/json",
                },

                body: JSON.stringify(jsonData),

            });

            const data = await response.json();     // get data response
            
            if (!response.ok) {    // If the response is not ok from the serializer

                openAlert("Algunos campos estan incompletos", "red", 1000);
                
                showErrorAlerts(data);        // If there is an accumulation of errors
                return;
            }
            
            // Redirect to specific url or to homre
            let url = "/";

            switch (actionType) {
                case "Login":
                    openAlert(data.message || "Login exitoso!", "green", 1000);
                    url = "/profile/"
                    break;

                case "Register":
                    openAlert(data.message || "Cuenta creada con exito!", "green", 1000);
                    url = "/profile/"
                    break;

                case "Close":
                    openAlert(data.message || "Sesión cerrada", "red", 1000);
                    break;
            
                default:
                    openAlert("Uknown action.", "red", 1000);
                    break;
            }

            // Redirect after a delay
            setTimeout(() => {
                window.location.href = url;
            }, 1000);

        } catch (error) {
            console.error("Error:", error);
            openAlert(`Error: ${error.message}`, "red", 2000);
        }
    });
}


function showErrorAlerts(errors, delay=1200) {
    let delay_total = 0;
    for (let field in errors) {
        if (errors.hasOwnProperty(field)) {
            errors[field].forEach((error) => {
                setTimeout(function() {
                    openAlert(`${field}: ${error}`, "red", delay);
                }, delay_total);

                // Incrementa el retraso para la siguiente alerta
                delay_total += delay; 
            });
        }
    }
}


// ============================================================================
//                Capture events of forms 
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
    // Captura el formulario de login
    const loginForm = document.getElementById('widget-register-form');
    if (loginForm) {
        handleFormActions(loginForm, "Login");
    } else {
        console.error("Form widget-register-form is not available.");
    }

    // Captura el formulario de cierre de sesión
    const closeSessionForm = document.getElementById('close-session');
    if (closeSessionForm) {
        handleFormActions(closeSessionForm, "Close");
    } else {
        console.error("Form close-session is not available.");
    }
});
