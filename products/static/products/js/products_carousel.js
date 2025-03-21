

/// <reference path="../../../../home/static/home/js/base.js" />

// ================================================================================
//                        Logica del tab de favoritos
// ================================================================================
// This creates a separate swiper instance for each element with the class "swiper-products"
document.querySelectorAll('.swiper-products').forEach((swiperContainer, index) => {
    const swiper = new Swiper(`#swiper-${index + 1}`, {
        loop: true, // Evita acumulación de slides mal posicionados
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
        slidesPerView: "auto", // Se ajusta con el CSS
        centeredSlides: false, // Evita que los slides se centren incorrectamente
        grabCursor: true,
        navigation: {
            nextEl: `#next-${index + 1}`,
            prevEl: `#prev-${index + 1}`,
        },
    });
});


// Function to add products with buttons sent as forms using the CSRF token
function formAddProductList() {
    document.querySelectorAll('.carousel-btn-carrito').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-index');
            handleCartActions(productId, 'add', 1);
        });
    });
};


// =========================================================================
//                        LIKES EFFECTS
// =========================================================================
function buttonLikeEvents() {
    // Selecciona todos los formularios de los botones "me gusta"
    document.querySelectorAll(".btn-like").forEach(button => {
        button.addEventListener('click', function() {

            if (AUTH_STATUS) {
                const productId = button.getAttribute("data-index");
                formButtonLikedProducts(button, productId);
            } else {
                openAlert('Debe logearse para guardar en Favoritos.', 'red', 2500);
            }
        });
    });
};


async function formButtonLikedProducts(button, productId) {
    try {
        // Realiza la solicitud POST usando Fetch
        const response = await fetch('/favorites-products/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                product_id: productId,
            })
        });

        const data = await response.json();  // Espera la respuesta JSON del servidor

        if (!response.ok) {
            openAlert(data.detail, 'red', 1500);
            return;
        }

        // Actualiza el botón de acuerdo con el estado
        const isLiked = button.classList.contains("liked");
        const icon = button.querySelector('i');
        if (isLiked) {
            button.classList.remove("liked");
            openAlert('Producto eliminado como Favorito.', 'red', 1500)
            icon.classList.replace("ri-heart-fill", "ri-heart-line");
        } else {
            button.classList.add("liked");
            openAlert('Producto agregado como Favorito!', 'green', 1500)
            icon.classList.replace("ri-heart-line", "ri-heart-fill");
        }
        
    } catch (error) {
        console.error('Error:', error);
    }
};


function imagesContainersEvents() {
    // Evento de clic en el contenedor de la imagen
    document.querySelectorAll('.image-container').forEach(image => {
        image.addEventListener('click', function () {
            const url = this.getAttribute('data-url');
            window.location.href = url;
        });
    });
};


function openModals() {
    const overlay = document.getElementById('overlay-carousel');

    // Configura los modales de productos
    document.querySelectorAll('.corner-box').forEach(button => {
        const modalId = button.getAttribute('data-modal-id');
        const modal = document.getElementById(modalId);

        if (modal) {
            setupToggleableElement({
                toggleButton: button,
                closeButton: modal.querySelector('.close-modal'),
                element: modal,
                overlay: overlay,
                flagStop: true,
            });
        }
    });
};


document.addEventListener('DOMContentLoaded', () => {
    imagesContainersEvents();
    openModals();
    formAddProductList();
    buttonLikeEvents();
});