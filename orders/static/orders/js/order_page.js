

// =====================================================================
//     Eventos del Payment y del envio
// =====================================================================
// Select all radio buttons with the name "payment"
const paymentButtons = document.querySelectorAll('input[name="payment"]');
const paymentSpans = document.querySelectorAll('.payment-method');
let idPayment = 0; // Stores the selected payment method ID

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


// =====================================================================
//                          Eventos de meotod de envio
// =====================================================================
// Retrieve shipping method elements
const shippingButtons = document.querySelectorAll('input[name="envio"]');
const shippinSpans = document.querySelectorAll('.shipment-method');
const shippinPriceSpan = document.getElementById('shipment-price');
let shippingMethodId = 0; // Stores selected shipping method ID

// Add change event listeners to each shipping option
shippingButtons.forEach(option => {
    option.addEventListener('change', (event) => {
        // Get selected method ID from data attribute
        // ID 1 = "Store Pickup", ID 2+ = other methods
        shippingMethodId = event.target.getAttribute('data-index');
        
        
        // Update form based on selection
        updateExtraForm(shippingMethodId);

        let price = getShippinPrice(event.target.dataset.price);  // Using dataset instead of getAttribute
        shippinPriceSpan.textContent = price === 'Gratis' ? price : `$ ${price}`;

        // Update all payment method displays
        shippinSpans.forEach(display => {
            display.textContent = event.target.value;
        });
        
        // Show success notification
        openAlert(`Método de envío actualizado a ${event.target.value}.`, 'green', 2000);
    });
});

function getShippinPrice(price) {
    // Convert the string value to a number
    const numericPrice = parseFloat(price);
    
    // Check if the price is 0
    if (numericPrice === 0) {
        return 'Gratis';
    }
    
    // Check if it's a whole number to remove .00
    if (Number.isInteger(numericPrice)) {
        return formatNumberWithCommas(price);
    }
    
    // Return the price with decimals if needed
    return numericPrice.toString();
}

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

        scrollToSection(extraFormContent);

    } catch (error) {
        console.error('Error:', error);
    }
}


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


    // get the form and send to validate
    const form = document.getElementById('form-order');
    validFormOrderWithAlerts(form)
});


// =============================================================================
//            Eventos para validar el formulario con la modal
// =============================================================================
// Función para manejar el formulario con validaciones y alertas
function validFormOrderWithAlerts(form) {

    form.addEventListener('submit', async function(event) {

        // Evita que el formulario se envíe de forma tradicional
        event.preventDefault(); 

        // Agregar los valores adicionales a los datos del formulario
        const formData = new FormData(form);
        formData.append('payment_method_id', idPayment);
        formData.append('envio_method_id', envioMethodId);  

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

            const data = await response.json(); // Procesar la respuesta como JSON

            if (!response.ok) {    // If the response is not ok from the serializer
                // showErrorAlerts(data);        // If there is an accumulation of errors
                openAlert("No hay suficiente stock para su carrito.", 'red', 1500);
                return;
            }

            if (!data.success) {
                openAlert("No hay suficiente stock para su carrito.", 'red', 1500);
                return;
            }

            // Función para mostrar alertas con mensajes de exito
            openAlert("Pedido guardado, complete su pago para retirar!", 'green', 2000);
            console.log(data.message);

            // Redirigir a la URL
            setTimeout(() => {
                window.location.href = '/payment_view/'; 
                // window.location.href = '/'; 
            }, 2000);

        } catch (error) {
            console.error('Error:', error);
            openAlert('Error al procesar la solicitud. Intenta nuevamente.', 'red', 2000);
        }
    });
}
