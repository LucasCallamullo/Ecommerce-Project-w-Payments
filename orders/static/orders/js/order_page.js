

// =====================================================================
//                          Eventos del Payment
// =====================================================================
// Selecciona todos los botones de radio con el mismo nombre
const paymentButtons = document.querySelectorAll('input[name="payment"]');
const paymentSpan = document.getElementById('payment-method')
let idPayment = 0

// Agrega un evento 'change' a cada botón de radio
paymentButtons.forEach(payment => {
    payment.addEventListener('change', (event) => {
        if (event.target.checked) {
            // Aquí puedes manejar el evento cuando el botón de radio está seleccionado
            paymentSpan.innerText = event.target.value
            openAlert('Método de pago actualizado.', 'green')
            idPayment = event.target.getAttribute('data-index');
        }
    });
});


// =====================================================================
//                          Eventos de meotod de envio
// =====================================================================
async function updateExtraForm(envioMethod) {
    try {
        const url = `/extra_form_ajax/?envioId=${encodeURIComponent(envioMethod)}`.replace(/\s+/g, '');
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();

        // realizar cambios en el contenedor
        const extraFormContent = document.getElementById('extra-form');
        extraFormContent.innerHTML = data.html;

    } catch (error) {
        console.error('Error:', error);
    }
}


// recuperar variables
const enviosButtons = document.querySelectorAll('input[name="envio"]');
const envioSpan = document.getElementById('envio-method')
const extraForm = document.getElementById('extra_form');
let envioMethodId = 0;


enviosButtons.forEach(envio => {
    envio.addEventListener('change', (event) => {

        // 1 para "Retiro en local", 2 o + para el resto son los id
        envioMethodId = event.target.getAttribute('data-index');
        
        // reemplazamos informacion 
        updateExtraForm(envioMethodId)
        envioSpan.innerText = event.target.value
        openAlert('Método de envío actualizado.', 'green')
    });
});


// =====================================================================
//                 Eventos del Modal para confirmar
// =====================================================================
const confirmButton = document.getElementById('confirm-order-btn');
const confirmButtonModal = document.getElementById('btn-confirm-order-modal');

// Función para abrir el modal
confirmButton.addEventListener('click', () => {
    flagsOrdersConfirm();
});


// Llamar a la función en el evento del botón de confirmación
confirmButtonModal.addEventListener('click', () => {
    flagsOrdersConfirm();

    console.log(idPayment, envioMethodId);

    if (idPayment == 0 || envioMethodId == 0) {
        openAlert('Te quedaste acá', 'red', 2000);
        return;
    }

    const modalOverlay2 = document.getElementById('modal-overlay');
    modalOverlay2.style.display = 'none';

    // Simula el clic en el botón submit oculto
    document.getElementById('submit-hidden').click();
});


// Función para manejar el formulario con validaciones y alertas
function validFormOrderWithAlerts(form) {

    form.addEventListener('submit', async function(event) {

        // Evita que el formulario se envíe de forma tradicional
        event.preventDefault(); 

        // Agregar los valores adicionales a los datos del formulario
        const formData = new FormData(form);
        formData.append('payment_id', idPayment);
        formData.append('envio_method_id', envioMethodId);

        console.log("aca paso algo malo");

        try {
            // Mandamos la solicitud fetch con la acción del formulario
            const response = await fetch(form.action, { 
                method: 'POST',
                body: formData,
                headers: {
                    // Asegúrate de enviar el token CSRF
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest' 
                }
            });

            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor.');
            }

            const data = await response.json(); // Procesar la respuesta como JSON

            if (data.success) {
                // Función para mostrar alertas (debe estar definida en tu proyecto)
                openAlert(data.message, 'green', 1000);
                console.log(data.message);

                // Redirigir a la URL proporcionada por la respuesta
                setTimeout(() => {
                    window.location.href = data.redirect_url; 
                }, 1000);

            } else {
                const message = data.error || 'Ocurrió un error inesperado.';
                openAlert(message, 'red', 2000);
                console.log(message);
            }

        } catch (error) {
            console.error('Error:', error);
            openAlert('Error al procesar la solicitud. Intenta nuevamente.', 'red', 2000);
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    // obtener el formulario y mandar a validarlo
    const form = document.getElementById('form-order');
    validFormOrderWithAlerts(form)
});


function flagsOrdersConfirm() {
    if ( idPayment == 0 ) {
        openAlert('Todavía no seleccionaste un método de pago.', 'red', 2000)
    } else if ( envioMethodId == 0 ) {
        openAlert('Todavía no seleccionaste un método de envío.', 'red', 2000)
    } else {
        const modalOverlay2 = document.getElementById('modal-overlay');
        modalOverlay2.style.display = 'flex';
    }
}


function modalEvents() {
    const orderButton = document.getElementById('order-btn');
    const modalOverlay = document.getElementById('modal-overlay');
    const closeModalButton = document.getElementById('close-modal');

    // Función para abrir el modal
    orderButton.addEventListener('click', () => {
        modalOverlay.style.display = 'flex';
    });

    // Función para cerrar el modal
    closeModalButton.addEventListener('click', () => {
        modalOverlay.style.display = 'none';
    });

    // Cerrar el modal haciendo clic fuera del contenido
    modalOverlay.addEventListener('click', (event) => {
        if (event.target === modalOverlay) {
            modalOverlay.style.display = 'none';
        }
    });
}

modalEvents()

