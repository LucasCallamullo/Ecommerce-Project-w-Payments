

/// <reference path="../../../../home/static/home/js/base.js" />


// ================================================================================
//                        Profile home Handle ajax 
// ================================================================================
/// <reference path="../../../../products/static/products/js/products_utils.js" />
/// <reference path="../../../../products/static/products/js/products_carousel.js" />
function initSwiperFavorites () { 
    // el nombre de la clase  es el que define a que swiper corresponde esta config
    const swiper = new Swiper(`#swiper-fav`, {
        loop: true, // Evita acumulación de slides mal posicionados
        autoplay: {
            delay: 6000,
            disableOnInteraction: false,
        },
        slidesPerView: "auto", // Se ajusta con el CSS
        centeredSlides: false, // Evita que los slides se centren incorrectamente
        grabCursor: true,
        navigation: {
            nextEl: `#next-fav`,
            prevEl: `#prev-fav`,
        },
    });
}

function onloadEventsTabs(dataContent) {
    if (dataContent === "Second Tab") {
        assignProductEvents();
        initSwiperFavorites();
    }
}


document.addEventListener('DOMContentLoaded', function () {
    const menuItems = document.querySelectorAll('.cover-menu li a');
    const contentDivs = {
        'First Tab': document.getElementById('first-tab'),
        'Second Tab': document.getElementById('second-tab'),
        'Third Tab': document.getElementById('third-tab'),
    };

    menuItems.forEach(item => {
        item.addEventListener('click', async function (e) {
            e.preventDefault();

            // Quitar clase 'active' de todos los elementos
            menuItems.forEach(i => i.parentElement.classList.remove('active'));
            this.parentElement.classList.add('active');

            const dataContent = this.getAttribute('data-content');
            const contentDiv = contentDivs[dataContent];

            // Oculta otros tabs y muestra el actual
            Object.values(contentDivs).forEach(div => div.style.display = 'none');
            contentDiv.style.display = 'block';

            try {
                const response = await fetch(`/profile/${dataContent.toLowerCase().replace(' ', '-')}/`);
                const data = await response.json();
            
                // Limpia el contenedor y añade un wrapper interno
                contentDiv.innerHTML = data.html; // Limpiar
            
                onloadEventsTabs(dataContent);
            } catch (error) {
                console.error('Error loading content:', error);
                contentDiv.innerHTML = '<p>Error loading content.</p>';
            }
        });
    });

    // Llama al clic del primer tab automáticamente al cargar la página
    const firstTab = menuItems[0];
    if (firstTab) {
        firstTab.click();
    }
});
