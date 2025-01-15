

function updateCartView(data) {

    const carritoTotal = document.getElementById('total-cart-view');
    const carritoTotal2 = document.getElementById('total-cart-view2');
    var precioTotal = formatNumberWithCommas(data.total);
    carritoTotal.textContent = `$${precioTotal}`;
    carritoTotal2.textContent = `$${precioTotal}`;
    
    // Reemplaza el contenido con el nuevo HTML
    const carritoContent = document.getElementById('cart-view-content');
    carritoContent.innerHTML = data.cart_view_html; 
    
    // Reasignar eventos después de actualizar el carrito
    assignCartViewButtonEvents();
}

function assignCartViewButtonEvents() {

    // Reasigna eventos a los botones de incremento
    document.querySelectorAll('.cart-view-plus').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-index');
            handleCartActions(productId, 'add', 1);
        });
    });

    // Reasigna eventos a los botones de decremento
    document.querySelectorAll('.cart-view-minus').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-index');
            handleCartActions(productId, 'less');
        });
    });

    // Reasignar botones delete
    document.querySelectorAll('.cart-view-btn-delete').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-index');
            // true es para actualizar la vista del carrito
            handleCartActions(productId, 'remove');
        });
    });
}

// Reasignar eventos al cargar la pagina
assignCartViewButtonEvents();