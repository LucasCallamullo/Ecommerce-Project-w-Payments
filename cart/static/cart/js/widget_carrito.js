

/* ==========================================================================================
                   "Función" para Eventos de mostrar y ocultar el carrito
========================================================================================== */
document.getElementById('cart-button').addEventListener('click', function() {
    document.getElementById('cart-container').classList.add('show');
    document.getElementById('overlay').classList.add('show');
});

document.getElementById('close-cart').addEventListener('click', function() {
    document.getElementById('cart-container').classList.remove('show');
    document.getElementById('overlay').classList.remove('show');
});

document.getElementById('overlay').addEventListener('click', function() {
    document.getElementById('cart-container').classList.remove('show');
    document.getElementById('overlay').classList.remove('show');
});


/* ==========================================================================================
                    Handle_Function para controlar los distintos eventos
========================================================================================== */
async function handleCartActions(productId, action, value = 1) {
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
                endpoint = '/carrito/add';
                break;
            case 'subtract':
                endpoint = '/carrito/subtract';
                break;
            case 'remove':
                endpoint = '/carrito/remove';
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
            body: new URLSearchParams(bodyParams)
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        // Handle interactive alert // remember, all responses have this data
        openAlert(data.message, data.color, 1000);    

        if (!data.flag_custom) return;    // This is a flag for verify some issues

        // This function update content with html responses
        updateCart(data);

        // show the cart widget if you dont are in the cart-page-view
        if ( !cartView ) {
            document.getElementById('cart-container').classList.add('show');
            document.getElementById('overlay').classList.add('show');
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
function updateCart(data) {
    // actualiza el badge total
    const badgeCantTotal = document.getElementById('badge-cart-button');
    badgeCantTotal.textContent = `${data.qty_total}`;

    const carritoTotal = document.getElementById('carrito-total');
    var precioTotal = formatNumberWithCommas(data.total);
    carritoTotal.textContent = `$${precioTotal}`;
    
    // Reemplaza el contenido con el nuevo HTML
    const carritoContent = document.getElementById('cart-content');
    carritoContent.innerHTML = data.widget_html; 
    
    // Reasignar eventos después de actualizar el carrito
    assignButtonEvents();
}

function formatNumberWithCommas(number) {
    // Convertir el número a string para trabajar con él
    var parts = number.toString().split(".");
    parts[0] = parts[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    // Unir la parte entera con la parte decimal, si existe
    return parts.join(".");
}


/* ==========================================================================================
                Función para asignar eventos a los botones
========================================================================================== */
function assignButtonEvents() {
    // Reasigna eventos a los botones de incremento
    document.querySelectorAll('.cart-item-btn-plus').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-index');
            const qty_add = 1;
            handleCartActions(productId, 'add', qty_add);
        });
    });

    // Reasigna eventos a los botones de decremento
    document.querySelectorAll('.cart-item-btn-minus').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-index');
            const qty_substract = 1;
            handleCartActions(productId, 'subtract', qty_substract);
        });
    });

    document.querySelectorAll('.cart-btn-remove-item').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-index');
            handleCartActions(productId, 'remove');
        });
    });
}

// Función para manejar la eliminación del ítem
function handleRemove(itemId) {
    const item = document.getElementById(itemId).closest('.cart-item');
    item.remove();
}

// Reasignar eventos al cargar la pagina
assignButtonEvents();


/* ==========================================================================================
// Función para obtener el valor del cookie por nombre actua como nuestro csrf token
========================================================================================== */
// Esta funcion se aplica en widget_carrito como en crud_to_cart.js de producto js
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Comprueba si el cookie tiene el nombre deseado
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                // Extrae y decodifica el valor del cookie
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


