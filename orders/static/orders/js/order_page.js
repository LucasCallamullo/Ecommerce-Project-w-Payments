

// =====================================================================
//        Eventos to Payments Methods
// =====================================================================
// Stores the selected payment method ID
let idPayment = 0; 

document.addEventListener('DOMContentLoaded', () => {
    // Select all radio buttons with the name "payment"
    const paymentButtons = document.querySelectorAll('input[name="payment"]');
    const paymentSpans = document.querySelectorAll('.payment-method');

    // Add 'change' event listener to each radio button
    paymentButtons.forEach(payment => {
        payment.addEventListener('change', (event) => {
            if (event.target.checked) {
                // Update all payment method displays
                paymentSpans.forEach(display => {
                    display.textContent = event.target.value;
                });
                
                // Show success alert with selected payment method
                openAlert(`Método de pago actualizado a ${event.target.value}.`, 'green', 2000);
                
                // Store the payment method ID from data attribute
                idPayment = event.target.getAttribute('data-index');
            }
        });
    });
});


// =====================================================================
//                          Shipping Method Events
// =====================================================================
// Stores selected shipping method ID
let shippingMethodId = 0; 

document.addEventListener('DOMContentLoaded', () => {
    // To update spans on column and into modal
    const shippingButtons = document.querySelectorAll('input[name="envio"]');
    const shippinSpans = document.querySelectorAll('.shipment-method');
    const shippinPriceSpan = document.getElementById('shipment-price');

    // To update additional form in the view
    const retireSection = document.getElementById('retire-form');
    const shippinSection = document.getElementById('shippin-form');

    // Add change event listeners to each shipping option
    shippingButtons.forEach(option => {
        option.addEventListener('change', (event) => {
            // Get selected method ID from data attribute
            // ID 1 = "Store Pickup", ID 2+ = other methods
            shippingMethodId = event.target.getAttribute('data-index');
            
            // Update form based on selection
            if ( shippingMethodId === '1' ) {
                retireSection.style.display = 'block';
                shippinSection.style.display = 'none';
                scrollToSection(retireSection);
            } else {
                retireSection.style.display = 'none';
                shippinSection.style.display = 'block';
                scrollToSection(shippinSection);
            }

            // Using dataset instead of getAttribute and Update all payment method displays
            let price = formatNumberWithPoints(event.target.dataset.price);  
            shippinPriceSpan.textContent = price === 'Gratis' ? price : `$ ${price}`;

            shippinSpans.forEach(display => {
                display.textContent = event.target.value;
            });
            
            // Show success notification
            openAlert(`Método de envío actualizado a ${event.target.value}.`, 'green', 2000);
        });
    });
});


// =============================================================================
//            Eventos para abrir el modal
// =============================================================================
document.addEventListener('DOMContentLoaded', () => {
    const btnOpenModal = document.getElementById('order-btn');
    const btnCloseModal = document.getElementById('close-modal');

    setupToggleableElement({
        toggleButton: btnOpenModal,
        closeButton: btnCloseModal,
        element: document.getElementById('modal-content'),
        overlay: document.getElementById('modal-overlay'),
    });

    const confirmButton = document.getElementById('confirm-order-btn');
    const confirmButtonModal = document.getElementById('btn-confirm-order-modal');
    let flagContinueModal = false;

    confirmButton.addEventListener('click', () => {
        flagContinueModal = flagsOrdersConfirm(); // Validate inputs
        if (!flagContinueModal) return; // Stop if validation fails
        
        btnOpenModal.click(); // Open modal if validation passes
    });

    confirmButtonModal.addEventListener('click', () => {
        btnCloseModal.click(); // Close the modal first
        
        flagContinueModal = flagsOrdersConfirm(); // Re-validate
        if (!flagContinueModal) return; // Stop if validation fails

        document.getElementById('submit-hidden').click(); // Submit form
    });

    
    const paymentSection = document.getElementById('payment-methods-section');
    const shippingSection = document.getElementById('shipping-methods-section');

    function flagsOrdersConfirm() {
        if (idPayment == 0) {
            openAlert('No seleccionaste un Método de Pago.', 'red', 2000);
            scrollToSection(paymentSection);
            return false;

        } else if (shippingMethodId == 0) {
            openAlert('No seleccionaste un Método de Envío.', 'red', 2000);
            scrollToSection(shippingSection)
            return false;
        }
        return true; // All validations passed
    }
});


// =============================================================================
//            Eventos para validar el formulario con la modal
// =============================================================================
document.addEventListener('DOMContentLoaded', () => {
    // get the form and send to validate
    const form = document.getElementById('form-order');
    validFormOrderWithAlerts(form)
});


// Función para manejar el formulario con validaciones y alertas
function validFormOrderWithAlerts(form) {

    form.addEventListener('submit', async function(event) {

        // Evita que el formulario se envíe de forma tradicional
        event.preventDefault(); 

        // Agregar los valores adicionales a los datos del formulario
        const formData = new FormData(form);
        formData.append('payment_method_id', idPayment);
        formData.append('shipping_method_id', shippingMethodId);  

        const jsonData = Object.fromEntries(formData.entries()); // Convertimos FormData en JSON

        try {
            // Mandamos la solicitud fetch con la acción del formulario
            const response = await fetch(form.action, { 
                method: 'POST',
                body: JSON.stringify(jsonData),
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    "Content-Type": "application/json",
                }
            });

            // Process the response as JSON
            const data = await response.json(); 

            // If the response is not ok from the serializer
            if (!response.ok) {    
                if ( data.success === 'stock' ) {
                    openAlert("No hay suficiente stock para su carrito.", 'red', 1500);
                    return;
                }

                if ( data.success === 'empty' ) {
                    openAlert("No hay items en tu carrito.", 'red', 1500);
                    return;
                }

                if ( data.success === 'error' ) {
                    openAlert(data.message || "ocurrio un error al crear la orden.", 'red', 1500);
                    return;
                }
                // If there is an accumulation of errors, but only we view one
                showErrorAlerts(data); 
                return;
            }

            // Bloquear clics en toda la página
            document.body.style.pointerEvents = "none";
            // Restaurar pointer-events antes de la redirección
            setTimeout(() => {
                document.body.style.pointerEvents = "auto";
            }, 1500);  

            // Función para mostrar alertas con mensajes de exito
            openAlert("Pedido guardado, complete su pago para finalizar!", 'green', 1500);
            console.log(data.message);

            // Redirigir a la URL
            setTimeout(() => {
                document.body.style.pointerEvents = "auto";
                window.location.href = `/payment-view/${data.order_id}/`;
            }, 1500);

        } catch (error) {
            console.error('Error:', error);
            openAlert('Error al procesar la solicitud. Intenta nuevamente.', 'red', 2000);
        }
    });
}


// Restaurar eventos al cargar la página
window.onload = () => {
    document.body.style.pointerEvents = "auto";
};