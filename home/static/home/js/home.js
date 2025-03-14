

// ================================================================================
//                        Swiper header
// ================================================================================
var swiperHeader = new Swiper('.swiper-container', {
    loop: true, // Infinite loop to continuously cycle through slides
    autoplay: {
      delay: 2500, // Time interval between slides (in milliseconds)
      disableOnInteraction: false, // Keep autoplay active even after user interaction
    },
    grabCursor: true, // Show grab cursor when hovering over the slider
    slidesPerView: 1, // Ensures only one slide is displayed at a time
    spaceBetween: 0, // Space between slides (adjust if needed)
    navigation: {
      nextEl: '.swiper-button-next', // Selector for the next slide button
      prevEl: '.swiper-button-prev', // Selector for the previous slide button
    },
    pagination: {
      el: '.swiper-pagination', // Selector for pagination bullets
      clickable: true, // Allows clicking on pagination bullets to navigate
    },
});


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



// Reasigna eventos a los botones de incremento

document.querySelectorAll('.carousel-btn-carrito').forEach(button => {
    
    button.addEventListener('click', function() {
        const productId = this.getAttribute('data-index');
        const qty_add = 1;
        handleCartActions(productId, 'add', qty_add);
    });
});


// ================================================================================
//                        Logica de imageness
// ================================================================================


document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll('.heart-button').forEach(button => {
    
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-index');
            
            if (AUTH_STATUS) {
                openAlert('uwu registrado', 'red')
            } else {
                openAlert('registrate boludo')
            }

        });
    });
});



// Evento de clic en el contenedor de la imagen
document.querySelectorAll('.image-container').forEach(image => {
    image.addEventListener('click', function () {
        const url = this.getAttribute('data-url');
        window.location.href = url;
    });
});



document.addEventListener("DOMContentLoaded", function () {

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
            });
        }
    });
});