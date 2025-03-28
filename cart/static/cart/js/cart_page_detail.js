

/// <reference path="../../../../home/static/home/js/base.js" />
/// <reference path="../../../../products/static/products/js/products_utils.js" />


function updateCartView(data) {

    const carritoTotal = document.getElementById('total-cart-view');
    const carritoTotal2 = document.getElementById('total-cart-view2');
    var precioTotal = formatNumberWithCommas(data.total);
    carritoTotal.textContent = `$${precioTotal}`;
    carritoTotal2.textContent = `$${precioTotal}`;
    
    // Reemplaza el contenido con el nuevo HTML
    const carritoContent = document.getElementById('cart-view-container');
    carritoContent.innerHTML = data.cart_view_html; 
    
    // Reasignar eventos después de actualizar el carrito
    assignBtnEvents();
}


// ==========================================================================
//        function to asign events
// ==========================================================================
function assignBtnEvents() {
    // funciones from products/products_utils.js" 
    document.querySelectorAll('.image-container').forEach(image => {
        imageContainerClickEvent(image);
    });

    document.querySelectorAll(".btn-like").forEach(button => {
        btnLikeProductEvent(button);
    });

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
            handleCartActions(productId, 'subtract');
        });
    });

    // Reasignar botones delete
    document.querySelectorAll('.cart-view-btn-delete').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-index');
            handleCartActions(productId, 'remove');
        });
    });
}


document.addEventListener('DOMContentLoaded', () => {
    assignBtnEvents();
});
