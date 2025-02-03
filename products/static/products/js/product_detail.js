

// ========================================================================
//            function buttons input and logic to add product
// ========================================================================
// Increment and decrement button handlers
function increment(button) {
    const input = button.closest('.quantity-container-detail').querySelector('#prod-input-qty');
    let currentValue = parseInt(input.value, 10);

    // Validar si el valor es un número válido
    if (isNaN(currentValue) || currentValue <= 0) {
        currentValue = 1
    } else {
        currentValue += 1;
    }
    input.value = currentValue;
}

function decrement(button) {
    const input = button.closest('.quantity-container-detail').querySelector('#prod-input-qty');
    let currentValue = parseInt(input.value, 10);

    // Validar si el valor es un número válido
    if (isNaN(currentValue) || currentValue <= 1) {
        currentValue = 1;
    } else {
        currentValue -= 1;
    }
    input.value = currentValue;
}


// Function to add products with buttons sent as forms using the CSRF token
document.getElementById('product-detail-form').addEventListener("submit", async function (event) {
    event.preventDefault(); // Prevent the form from submitting the traditional way

    // Correctly accessing the product_id
    const productId = this.querySelector('input[name="product_id"]').value;

    // Get quantity of the product
    const input = document.getElementById('prod-input-qty');
    let currentValue = parseInt(input.value, 10);
    
    // Simple validation check
    if (isNaN(currentValue) || currentValue <= 0) {
        // This generic function is called from home/base/base.js
        openAlert('Ingrese un numero válido.', 'red', 1000);
        return;
    }

    // This function is called from cart/widget_carrito.js
    handleCartActions(productId, 'add', currentValue);
});


// ========================================================================
//               Para cambiar las imagens del contenedor main
// ========================================================================
document.querySelectorAll(".prod-small-image-container").forEach(container => {
    container.addEventListener("click", function () {

        // Eliminar la clase 'active' de todos los contenedores
        document.querySelectorAll(".prod-small-image-container").forEach(item => {
            item.classList.remove("active");
        });

        // Agregar la clase 'active' al contenedor de la imagen clickeada
        container.classList.add("active");

        // Reemplazar la img en la contenedor main
        const image = container.querySelector(".prod-small-image");
        if (image) {
            const imageUrl = image.src;
            document.getElementById("prod-main-image").src = imageUrl;
        }
    });
});


document.addEventListener("DOMContentLoaded", function () {
    // Seleccionar el primer contenedor de imagen y agregarle la clase 'active'
    const firstContainer = document.querySelector(".prod-small-image-container");
    if (firstContainer) {
        firstContainer.classList.add("active");
    }
    // Seleccionamos todas las imágenes pequeñas
    const smallImages = document.querySelectorAll(".prod-small-image-container");
    let currentIndex = 0; // Índice de la imagen actual

    // Función para cambiar la imagen principal
    function changeMainImage(index) {
        const imageUrl = smallImages[index].querySelector(".prod-small-image").src;
        document.getElementById("prod-main-image").src = imageUrl;

        // Actualizar la clase 'active' en la imagen seleccionada
        smallImages.forEach((container) => {
            container.classList.remove("active");
        });
        smallImages[index].classList.add("active");
    }

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


// Efectos de zoom
window.onload = () => {
    const overlay = document.getElementById('fullscreen-overlay');
    const productId = parseInt(overlay.getAttribute('data-index'), 10);
    const imageContainer = document.getElementById('image-container');
    const zoomButton = document.getElementById('zoom-button');
    const leftArrow = document.querySelector('.left-overlay');
    const rightArrow = document.querySelector('.right-overlay');
    let currentIndex = 0;
    let images = [];
    let isZoomed = false;       // Estado del zoom
    let isDragging = false;     // Estado del arrastre
    let startX, startY;         // Posiciones iniciales del mouse
    let offsetX = 50, offsetY = 50;     // Posición inicial del fondo (en porcentaje)

    // Consultar el endpoint para obtener las imágenes
    fetch(`/products-images/${productId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.images && data.images.length > 0) {
                images = data.images;
                console.log(images)
                updateBackgroundImage(); // Cargar la primera imagen como fondo
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
        imageContainer.style.backgroundSize = isZoomed ? '200%' : 'contain'; // Ajustar tamaño del fondo
        imageContainer.style.backgroundPosition = `${offsetX}% ${offsetY}%`; // Posición inicial
    }

    // Navegar a la imagen anterior
    leftArrow.addEventListener('click', () => {
        currentIndex = (currentIndex - 1 + images.length) % images.length;
        resetZoomAndDrag(); // Restablece el estado de zoom y arrastre
        updateBackgroundImage();
    });

    // Navegar a la imagen siguiente
    rightArrow.addEventListener('click', () => {
        currentIndex = (currentIndex + 1) % images.length;
        resetZoomAndDrag(); // Restablece el estado de zoom y arrastre
        updateBackgroundImage();
    });

    // Abrir la imagen en pantalla completa
    zoomButton.addEventListener('click', () => {
        overlay.style.display = 'flex'; // Muestra el contenedor
        resetZoomAndDrag(); // Restablece el estado
    });

    // Cerrar la pantalla completa al hacer clic en el fondo oscuro
    overlay.addEventListener('click', (event) => {
        if (event.target === overlay) {
            overlay.style.display = 'none'; // Oculta el contenedor
            imageContainer.classList.remove('zoom-out-cursor'); // Restaura el cursor
            imageContainer.classList.add('zoom-in-cursor'); // Restaura el cursor
            resetZoomAndDrag(); // Restablece el estado de zoom y arrastre
        }
    });

    // Hacer zoom al hacer clic en el contenedor
    imageContainer.addEventListener('click', (event) => {
        if (isZoomed && isDragging) {
            imageContainer.classList.remove('zoom-out-cursor'); // Restaura el cursor
            imageContainer.classList.add('zoom-in-cursor'); // Restaura el cursor
            resetZoomAndDrag();
            return;
        }

        isDragging = true;
        startX = event.clientX;
        startY = event.clientY;
        imageContainer.classList.remove('zoom-in-cursor'); // Restaura el cursor
        imageContainer.classList.add('zoom-out-cursor'); // Restaura el cursor

        isZoomed = !isZoomed; // Alternar el estado de zoom

        // Cambiar el tamaño del fondo
        imageContainer.style.backgroundSize = isZoomed ? '200%' : 'contain'; 
        offsetX = 50; // Restablecer posición del fondo al centro
        offsetY = 50;
        imageContainer.style.backgroundPosition = `${offsetX}% ${offsetY}%`; // Aplicar la posición inicial
    });

    window.addEventListener('mousemove', (event) => {
        if (isDragging && isZoomed) {
            const deltaX = event.clientX - startX;
            const deltaY = event.clientY - startY;

            // Ajustar la posición del fondo basado en el movimiento del mouse
            offsetX = Math.min(Math.max(offsetX + deltaX / 5, 0), 100); // Limitar entre 0% y 100%
            offsetY = Math.min(Math.max(offsetY + deltaY / 5, 0), 100); // Limitar entre 0% y 100%

            imageContainer.style.backgroundPosition = `${offsetX}% ${offsetY}%`;

            startX = event.clientX;
            startY = event.clientY;
        }
    });

    function resetZoomAndDrag() {
        isZoomed = false;
        isDragging = false;
        offsetX = 50; // Centrar la imagen
        offsetY = 50;
        updateBackgroundImage();
    }
};
