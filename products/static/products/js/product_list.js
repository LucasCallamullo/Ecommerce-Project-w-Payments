




// ==========================================================================
//         AJAX FOR CARDS PRESENTED IN THE product_list
// ==========================================================================
let make_filter = false;    // for revert the filter

function updateProductListFromInput() {
    // Retrieve the filters directly from the container
    const filtersElement = document.getElementById('filters');
    const filters = filtersElement.dataset;
    
    const searchInput = document.getElementById('search-input');

    // Access filters directly (data-category-id --> categoryId, automatically camelCase)
    // Default values are assigned in case they don't exist, useful for logic with '0'
    const categoryId = filters.categoryId || '';
    const subCategoryId = filters.subCategoryId || '';
    const topQuery = filters.topQuery || '';
    const inputNow = searchInput.value;

    // For cases where the filter should be reset
    if (make_filter && inputNow.length < 3) {
        make_filter = false;
        updateProductList('', topQuery, categoryId, subCategoryId);
        return;
    }

    // Check if the input length is >= 3 before proceeding
    if (inputNow.length < 3) return;

    // 300ms timer to avoid multiple queries
    let debounceTimer;
    clearTimeout(debounceTimer);

    debounceTimer = setTimeout(function() {
        updateProductList(inputNow, topQuery, categoryId, subCategoryId);
        make_filter = true;
    }, 300);
};


async function updateProductList(inputNow, topQuery, categoryId, subCategoryId) {
    try {
        const url = `/products-search/?inputNow=${encodeURIComponent(inputNow)}
        &topQuery=${encodeURIComponent(topQuery)}&categoryId=${encodeURIComponent(categoryId)}
        &subCategoryId=${encodeURIComponent(subCategoryId)}`.replace(/\s+/g, '');

        console.log('Request URL:', url); // Verify the generated URL

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        
        // Make changes in the container and reassign events
        const carritoContent = document.getElementById('search-results');
        carritoContent.innerHTML = data.html_cards;

        // Reassign form events
        imagesContainersEvents();
        openModals();
        formAddProductList();
        buttonLikeEvents();
            
    } catch (error) {
        console.error('Error:', error);
    }
}


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



// Function to add products with buttons sent as forms using the CSRF token
function formAddProductList() {
    document.querySelectorAll('.prod-extender-btn').forEach(form => {
        form.addEventListener("submit", async function (event) {
            event.preventDefault(); 
            
            // Correctly accessing the product_id
            const productId = form.querySelector('input[name="product_id"]').value;
            handleCartActions(productId, 'add', 1); 
        });
    });
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
    const overlay = document.getElementById('overlay-products-modal');

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



