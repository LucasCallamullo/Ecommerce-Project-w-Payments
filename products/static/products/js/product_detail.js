

/// <reference path="../../../../home/static/home/js/base.js" />

// ========================================================================
//            function buttons input and logic to add product
// =======================================================================
document.addEventListener("DOMContentLoaded", function () {
    // Seleccionar los botones de incremento y decremento
    const incrementButton = document.querySelector('.prodd-btn-plus');
    const decrementButton = document.querySelector('.prodd-btn-minus');

    // Verificar si los botones existen antes de agregar los eventos
    if (incrementButton && decrementButton) {
        // Agregar evento de clic al botón de incremento
        incrementButton.addEventListener('click', function () {
            increment(this);
        });

        // Agregar evento de clic al botón de decremento
        decrementButton.addEventListener('click', function () {
            decrement(this);
        });
    }

    // Función para incrementar el valor
    function increment(button) {
        const input = button.closest('.product-container-conts').querySelector('#prod-input-qty');
        let currentValue = parseInt(input.value, 10);

        // Validar si el valor es un número válido
        if (isNaN(currentValue) || currentValue <= 0) {
            currentValue = 1;
        } else {
            currentValue += 1;
        }
        input.value = currentValue;
    }

    // Función para decrementar el valor
    function decrement(button) {
        const input = button.closest('.product-container-conts').querySelector('#prod-input-qty');
        let currentValue = parseInt(input.value, 10);

        // Validar si el valor es un número válido
        if (isNaN(currentValue) || currentValue <= 1) {
            currentValue = 1;
        } else {
            currentValue -= 1;
        }
        input.value = currentValue;
    }
});

// Function to add products with buttons sent as forms using the CSRF token
document.getElementById('product-detail-form').addEventListener("submit", async function (event) {
    event.preventDefault();

    const productId = this.getAttribute('data-index');

    const input = document.getElementById('prod-input-qty');
    let currentValue = parseInt(input.value, 10);
    
    if (isNaN(currentValue) || currentValue <= 0) {
        openAlert('Ingrese un numero válido.', 'red', 1000);
        return;
    }

    handleCartActions(productId, 'add', currentValue);
});



// ========================================================================
//               Para cambiar las imágenes del contenedor main
// ========================================================================
document.addEventListener("DOMContentLoaded", function () {
    // Seleccionar todas las imágenes pequeñas
    const smallImages = document.querySelectorAll(".prod-small-image-container");
    let currentIndex = 0; // Índice de la imagen actual

    // Función para cambiar la imagen principal
    function changeMainImage(index) {
        // Actualizar el índice actual
        currentIndex = index;

        // Obtener la URL de la imagen pequeña seleccionada
        const imageUrl = smallImages[index].querySelector(".prod-small-image").src;
        document.getElementById("prod-main-image").src = imageUrl;

        // Actualizar la clase 'active' en la imagen seleccionada
        smallImages.forEach((container, i) => {
            if (i === index) {
                container.classList.add("active");
            } else {
                container.classList.remove("active");
            }
        });
    }

    // Agregar evento de clic a cada imagen pequeña
    smallImages.forEach((container, index) => {
        container.addEventListener("click", function () {
            changeMainImage(index); // Cambiar la imagen principal al hacer clic
        });
    });

    // Flecha izquierda
    document.querySelector(".arrow-button.left").addEventListener("click", function () {
        if (currentIndex > 0) {
            currentIndex--; // Disminuir el índice
        } else {
            currentIndex = smallImages.length - 1; // Volver a la última imagen
        }
        changeMainImage(currentIndex);
    });

    // Flecha derecha
    document.querySelector(".arrow-button.right").addEventListener("click", function () {
        if (currentIndex < smallImages.length - 1) {
            currentIndex++; // Aumentar el índice
        } else {
            currentIndex = 0; // Volver a la primera imagen
        }
        changeMainImage(currentIndex);
    });

    // Inicializar la primera imagen
    changeMainImage(currentIndex);
});



// ========================================================================
//               Wsp Button Generic
// ========================================================================
document.addEventListener('DOMContentLoaded', function () {
    const productLink = document.getElementById('whatsapp-link');

    // Obtén el número de teléfono desde el atributo data-cellphone
    const cellphone = productLink.getAttribute('data-wsp');
    const productName = productLink.getAttribute('data-name');
    
    // Formatear el número y generar el enlace de WhatsApp
    const whatsappUrl = formatPhoneNumber(cellphone);

    // Crea el mensaje dinámicamente con los valores del producto
    const message = `Buenos días me interesa el ${productName} 
    1- Quería consultar sobre formas de pago con tarjeta en el local?
    2- Consultar sobre tipos de envío o formas de retiro?`;

    // Si el número es válido, concatenamos la URL con el mensaje
    if (whatsappUrl) {
        const finalWhatsappUrl = `${whatsappUrl}?text=${encodeURIComponent(message)}`;
        
        // Asigna el nuevo enlace con el mensaje al atributo href
        productLink.setAttribute('href', finalWhatsappUrl);

        // Assign href generic to the float btn-wsp
        const productLinkBase = document.getElementById('wsp-link');
        productLinkBase.setAttribute('href', finalWhatsappUrl);
    }
});


// ========================================================================
//               Zoom effects
// ========================================================================
window.onload = () => {
    const overlay = document.getElementById('fullscreen-overlay');
    const productId = parseInt(overlay.getAttribute('data-index'), 10);
    const imageContainer = document.getElementById('image-container');
    const zoomButton = document.getElementById('zoom-button');
    const leftArrow = document.querySelector('.left-overlay');
    const rightArrow = document.querySelector('.right-overlay');

    const cornerZoom = document.querySelector('.zoom-corner');
    
    const zoomInIcon = overlay.getAttribute('data-zoom-in');
    const zoomOutIcon = overlay.getAttribute('data-zoom-out');

    let currentIndex = 0;
    let images = [];
    let isZoomed = false;
    let isDragging = false;
    let startX, startY;
    let offsetX = 50, offsetY = 50;

    // Obtener las imágenes del producto
    fetch(`/products-images/${productId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.images && data.images.length > 0) {
                images = data.images;
                updateBackgroundImage();
            } else {
                console.error("No images found for this product.");
            }
        })
        .catch(error => {
            console.error("Error fetching images:", error);
        });

    // Actualizar la imagen de fondo
    function updateBackgroundImage() {
        imageContainer.style.backgroundImage = `url(${images[currentIndex]})`;
        imageContainer.style.backgroundSize = isZoomed ? '200%' : '100%';
        imageContainer.style.backgroundPosition = `${offsetX}% ${offsetY}%`;
    }

    // Cambiar el cursor según el estado del zoom
    function updateCursor() {
        if (isZoomed) {
            imageContainer.style.cursor = `url('${zoomOutIcon}'), auto`; // Cursor de zoom out
        } else {
            imageContainer.style.cursor = `url('${zoomInIcon}'), auto`; // Cursor de zoom in
        }
    }

    // Restablecer el estado de zoom y arrastre
    function resetZoomAndDrag() {
        isZoomed = false;
        isDragging = false;
        offsetX = 50;
        offsetY = 50;
        updateBackgroundImage();
        updateCursor();
    }

    // Navegar a la imagen anterior
    leftArrow.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        resetZoomAndDrag();
        updateBackgroundImage();
    });

    // Navegar a la imagen siguiente
    rightArrow.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % images.length;
        resetZoomAndDrag();
        updateBackgroundImage();
    });

    // Abrir la imagen en pantalla completa
    zoomButton.addEventListener('click', () => {
        overlay.style.display = 'flex';
        resetZoomAndDrag();
    });

    // Cerrar la pantalla completa al hacer clic en el fondo oscuro
    overlay.addEventListener('click', (event) => {
        if (event.target === overlay) {
            overlay.style.display = 'none';
            resetZoomAndDrag();
        }
    });

    // Hacer zoom al hacer clic en el contenedor
    cornerZoom.addEventListener('click', (event) => {
        imageContainer.click();
    });

    imageContainer.addEventListener('click', (event) => {
        if (isZoomed && isDragging) {
            resetZoomAndDrag();
            return;
        }

        isDragging = true;
        startX = event.clientX;
        startY = event.clientY;

        isZoomed = !isZoomed;
        updateBackgroundImage();
        updateCursor();
    });

   // Función para manejar el inicio del arrastre (ratón y toque)
    function startDrag(event) {
        if (isZoomed) {
            isDragging = true;

            // Obtener las coordenadas iniciales
            if (event.type === 'touchstart') {
                event.preventDefault(); // Evitar el desplazamiento de la página
                startX = event.touches[0].clientX;
                startY = event.touches[0].clientY;
            } else {
                startX = event.clientX;
                startY = event.clientY;
            }
        }
    }

    // Función para manejar el movimiento durante el arrastre (ratón y toque)
    function moveDrag(event) {
        if (isDragging && isZoomed) {
            let clientX, clientY;

            // Obtener las coordenadas actuales
            if (event.type === 'touchmove') {
                event.preventDefault(); // Evitar el desplazamiento de la página
                clientX = event.touches[0].clientX;
                clientY = event.touches[0].clientY;
            } else {
                clientX = event.clientX;
                clientY = event.clientY;
            }

            // Calcular el desplazamiento
            const deltaX = clientX - startX;
            const deltaY = clientY - startY;

            // Actualizar la posición del fondo
            offsetX = Math.min(Math.max(offsetX + deltaX / 5, 0), 100);
            offsetY = Math.min(Math.max(offsetY + deltaY / 5, 0), 100);

            imageContainer.style.backgroundPosition = `${offsetX}% ${offsetY}%`;

            // Actualizar las coordenadas iniciales
            startX = clientX;
            startY = clientY;
        }
    }


    // Función para manejar el fin del arrastre (ratón y toque)
    function endDrag() {
        isDragging = false;
    }

    // Eventos para ratón
    imageContainer.addEventListener('mousedown', startDrag);
    window.addEventListener('mousemove', moveDrag);
    window.addEventListener('mouseup', endDrag);

    // Eventos para toque
    imageContainer.addEventListener('touchstart', startDrag, { passive: false });
    window.addEventListener('touchmove', moveDrag, { passive: false });
    window.addEventListener('touchend', endDrag);

};