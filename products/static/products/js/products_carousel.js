

/// <reference path="../../../../home/static/home/js/base.js" />
/// <reference path="../../../../products/static/products/js/products_utils.js" />


// ================================================================================
//                        Logica del tab de favoritos
// ================================================================================
function initSwipers() { 
    // This creates a separate swiper instance for each element with the class "swiper-products"
    document.querySelectorAll('.swiper-products').forEach((swiperContainer, index) => {
        const swiper = new Swiper(`#swiper-${index + 1}`, {
            loop: true, // Evita acumulación de slides mal posicionados
            autoplay: {
                delay: 6000,
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
}

document.addEventListener('DOMContentLoaded', () => {
    initSwipers();
});


// =========================================================================
//                        Assign Events
// =========================================================================
function assignProductEvents() {
    document.querySelectorAll(".btn-like").forEach(button => {
        btnLikeProductEvent(button);
    });

    document.querySelectorAll('.carousel-extender-btn').forEach(form => {
        formToAddProducts(form, 1);
    });

    document.querySelectorAll('.image-container').forEach(image => {
        imageContainerClickEvent(image);
    });

    const overlay = document.getElementById('overlay-carousel');
    document.querySelectorAll('.corner-box').forEach(button => {
        openProductModal(overlay, button)
    });
};

document.addEventListener('DOMContentLoaded', () => {
    assignProductEvents();
});