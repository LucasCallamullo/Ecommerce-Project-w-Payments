

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
                   "Función" para Eventos de mostrar y ocultar alertas de los items
========================================================================================== */
// Mostrar la alerta
function openAlert(message, action) {
    const alertBox = document.getElementById('alertBox');
    alertBox.querySelector('.alert-message').textContent = message; // Agrega el mensaje dinámico
    
    // Elimina cualquier clase previa para evitar conflictos
    alertBox.classList.remove('alert-green', 'alert-red');

    // Agrega la clase correspondiente según la acción
    if (action === 'remove' || message === 'Producto eliminado de tu carrito.' ) {
        alertBox.classList.add('alert-red');
    } else {
        alertBox.classList.add('alert-green');
    }

    // Muestra la alerta
    alertBox.classList.add('show');
    alertBox.classList.remove('hidden');

    // Inicia un temporizador para cerrar la alerta después de 2 segundos
    setTimeout(closeAlert, 1000); // 1000 ms = 1 segundos
}

// Cerrar la alerta
function closeAlert() {
    const alertBox = document.getElementById('alertBox');
    alertBox.classList.remove('show');
    alertBox.classList.add('hidden');
}


/* ==========================================================================================
                    Handle_Function para controlar los distintos eventos
========================================================================================== */
async function handleCartActions(productId, action, value=1) {
    try {
        // Verificamos si estamos en la página del carrito antes de mostrar el carrito y overlay
        const currentPage = window.location.pathname;
        const cart_view = ( currentPage == '/ver-carrito/' );

        const response = await fetch('/carrito/update/', {
            method: 'POST',     // Especifica que el método de la solicitud es POST
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded', // Indica el tipo de contenido de los datos enviados
                'X-CSRFToken': getCookie('csrftoken') // Añade el token CSRF a los encabezados para la seguridad
            },
            body: new URLSearchParams({
                'producto_id': productId, // Envía el ID del producto como parte del cuerpo de la solicitud
                'action': action,    // 'add', 'less', 'remove'
                'value': value,    // value for quantity
                'cart_view': cart_view ? 'true':'false'   // cart_view for cart_view update
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        // Muestra una alerta con el mensaje del servidor
        openAlert(data.message, action);

        // Si no hay stock suficiente, termina aquí
        if (!data.flag_stock) return;

        // Actualiza la vista del WDIGET carrito con los datos más recientes
        updateCart(data);

        // Muestra el carrito y el overlay si no estas en la pagina del carrito
        if ( !cart_view ) {
            document.getElementById('cart-container').classList.add('show');
            document.getElementById('overlay').classList.add('show');
        }

        // Actualiza la VIEW del carrito con los datos más recientes
        // typeof == solo ejecuta la funcion si esta definida en mi contexto actual
        if (cart_view && typeof updateCartView === 'function') {
            updateCartView(data);
        }

    } catch (error) {
        console.error('Error:', error); // Maneja y muestra cualquier error en la consola
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
            handleCartActions(productId, 'less');
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
    // Lógica para eliminar el ítem del carrito
    // alert('Ítem eliminado');
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


