

/// <reference path="../../../../home/static/home/js/base.js" />


/* ==========================================================================================
                   "Función" para Eventos de mostrar y ocultar el carrito
========================================================================================== */
document.addEventListener('DOMContentLoaded', () => {

    // Define the pages where the functionality should NOT be activated
    const blockedPages = [
        "/order/",      // Blocked page: order page
        "/payment-view/" // Blocked page: payment view page
    ];

    // Get the current path of the page
    const currentPath = window.location.pathname;

    // If the current page is in the blocked pages list, prevent functionality
    if (blockedPages.includes(currentPath)) {
        // Add a click event listener to each cart button that shows an alert
        const cartButtons = document.querySelectorAll('.cart-button');

        cartButtons.forEach((cartButton) => {
            cartButton.addEventListener('click', () => {
                openAlert('No puedes usar el Carrito durante el pedido y/o pago.', 'green', 2000);
            });
        });

        // Exit the function early to prevent the rest of the code from executing
        return;
    }

    // Retrieve all the cart buttons and their corresponding cart containers
    const cartButtons = document.querySelectorAll('.cart-button');
    const cartContainers = document.querySelectorAll('.cart-cont-overlay');
    const cartOverlays = document.querySelectorAll('.cart-overlay');
    const cartBtnCloses = document.querySelectorAll('.close-widget-cart');

    // Check if the number of buttons matches the number of cart containers
    if (cartButtons.length !== cartContainers.length) {
        console.error('The number of buttons and cart containers does not match.');
    }

    // Associate each button with its corresponding elements (containers, overlays, etc.)
    cartButtons.forEach((cartButton, index) => {
        const cartContainer = cartContainers[index];
        const overlay = cartOverlays[index];
        const buttonClose = cartBtnCloses[index];

        // Setup the toggleable elements with the given configuration
        setupToggleableElement({
            toggleButton: cartButton,
            closeButton: buttonClose,
            element: cartContainer,
            overlay: overlay,
        });
    });
});



/* ==========================================================================================
                    Handle_Function para controlar los distintos eventos
========================================================================================== */
async function handleCartActions(productId, action, value=1) {
    try {
        // Verificamos si estamos en la página del carrito
        const currentPage = window.location.pathname;
        const cartView = (currentPage === '/ver-carrito/');

        let endpoint = ''; // Endpoint por defecto
        let bodyParams = {
            'productId': productId,
            'quantity': value,
            'cartView': cartView ? 'true' : 'false'
        };

        // Depend of the action we can call some endpoint
        switch (action) {
            case 'add':
                endpoint = '/carrito/add/';
                break;
            case 'subtract':
                endpoint = '/carrito/subtract/';
                break;
            case 'remove':
                endpoint = '/carrito/remove/';
                break;
            default:
                throw new Error('Acción desconocida');
        }

        // Se realiza el fetch según el endpoint de la acción
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: new URLSearchParams(bodyParams),
            credentials: 'include',  // Asegúrate de incluir las credenciales si es necesario
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        // Handle interactive alert // remember, all responses have this data
        openAlert(data.message, data.color, 1000);    

        if (!data.flag_custom) return;    // This is a flag for verify some issues

        // This function update content with html responses
        let index;
        if (window.innerWidth <= 992) {
            // Mobile: Activar el botón con index 0
            index = 0;
        } else {
            // Desktop: Activar el botón con index 1
            index = 1;
        }

        updateCart(data, index);

        // show the cart widget if you dont are in the cart-page-view
        if ( !cartView ) {
            const cartContainers = document.querySelectorAll('.cart-cont-overlay');
            let isOpenCart = cartContainers[index].getAttribute('data-state') === 'open';

            if ( !isOpenCart ) {
                const cartButtons = document.querySelectorAll('.cart-button');
                cartButtons[index].click();
            } else {
                console.log('estaba abierto xd')
            }
        }

        // if you are in the cart-view-page update the view
        // typeof == only use the function if is define in my current context
        if (cartView && typeof updateCartView === 'function') {
            updateCartView(data);
        }

    } catch (error) {
        console.error('Error:', error);
    }
}


/* ==========================================================================================
                    Función para actualizar la vista del carrito
========================================================================================== */
function updateCart(data, index) {
    // Mobile: Activar el botón con index 0    // Desktop: Activar el botón con index 1
    if (index === 1) {
        const badgeCantTotal = document.getElementById('badge-cart-button');
        badgeCantTotal.textContent = `${data.qty_total}`;
    }
    
    const cartTotals = document.querySelectorAll('.cart-w-total');
    const cartContainers = document.querySelectorAll('.cart-content');

    const cartTotal = cartTotals[index];
    const cartContent = cartContainers[index];

    var totalPrice = formatNumberWithPoints(data.total);
    cartTotal.textContent = `$${totalPrice}`;

    // Reemplaza el contenido con el nuevo HTML
    cartContent.innerHTML = data.widget_html;

    // Reasignar eventos después de actualizar el carrito
    assignButtonEvents();
}


/* ==========================================================================================
                Función para asignar eventos a los botones
========================================================================================== */
function assignButtonEvents() {
    // Reasigna eventos a los botones de incremento
    document.querySelectorAll('.cart-item-btn-plus').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-index');
            handleCartActions(productId, 'add', 1);
        });
    });

    // Reasigna eventos a los botones de decremento
    document.querySelectorAll('.cart-item-btn-minus').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-index');
            handleCartActions(productId, 'subtract', 1);
        });
    });

    document.querySelectorAll('.cart-item-btn-remove').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-index');
            handleCartActions(productId, 'remove');
        });
    });
}

// Reasignar eventos al cargar la pagina
assignButtonEvents();








