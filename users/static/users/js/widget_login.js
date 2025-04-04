

/// <reference path="../../../../home/static/home/js/base.js" />

// ========================================================================
//                   Evento de clic en el botón de usuario
// ========================================================================
document.addEventListener('DOMContentLoaded', () => {

    // Recupera todos los botones y dropdowns
    const userButtons = document.querySelectorAll('.user-button');
    const dropdowns = document.querySelectorAll('.user-dropdown');

    // Verifica que haya la misma cantidad de botones y dropdowns
    if (userButtons.length !== dropdowns.length) {
        console.error('La cantidad de botones y dropdowns no coincide.');
    }

    // Asocia cada botón con su dropdown correspondiente
    userButtons.forEach((userLoginButton, index) => {
        const dropdown = dropdowns[index]; // Dropdown correspondiente

        userLoginButton.addEventListener('click', function (event) {
            event.stopPropagation(); // Evita que el evento se propague

            const isExpanded = userLoginButton.getAttribute('aria-expanded') === 'true';
            // retorna false y false != true --> isExpanded queda en false
            userLoginButton.setAttribute('aria-expanded', !isExpanded);

            // Cambia el estado del dropdown
            toggleState(dropdown);

            // Evita que el dropdown se cierre al hacer clic dentro de él
            dropdown.addEventListener('click', function (event) {
                event.stopPropagation();
            });
        });
    });

    // Evento de clic en cualquier parte del documento
    document.addEventListener('click', function (event) {
        userButtons.forEach((userLoginButton, index) => {
            const dropdown = dropdowns[index]; // Dropdown correspondiente

            // Verifica si el clic no se hizo dentro del dropdown ni del botón
            if ( !dropdown.contains(event.target) ) {
                const isExpanded = userLoginButton.getAttribute('aria-expanded') === 'true';
                if (isExpanded) {
                    // Cambia el estado del dropdown
                    toggleState(dropdown);
                    userLoginButton.setAttribute('aria-expanded', !isExpanded);
                }
            }
        });
    });
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




// ============================================================================
//                Capture events of forms 
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
    // Captura el formulario de login
    
    const formsRegister = document.querySelectorAll('.widget-register-form')
    formsRegister.forEach((form) => {
        if (form) {
            handleFormActions(form, "Login");
        } else {
            console.error("Form widget-register-form is not available.");
        }
    });

    // Captura el formulario de cierre de sesión
    const formsClose = document.querySelectorAll('.widget-close-form')
    formsClose.forEach((form) => {
        if (form) {
            handleFormActions(form, "Close");
        } else {
            console.error("Form close-session is not available.");
        }
    });
});
