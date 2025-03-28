

/// <reference path="../../../../home/static/home/js/base.js" />


/**
 * Sends a POST request to toggle a product's "liked" (favorite) status 
 * and updates the button's appearance accordingly.
 * 
 * @param {HTMLElement} button - The button element associated with the product like action.
 * @param {string|number} productId - The ID of the product to be liked/unliked.
 * 
 * Behavior:
 * - Sends an asynchronous POST request to the `/favorites-products/` endpoint, including the product ID in the body.
 * - The CSRF token is retrieved via the helper function `getCookie('csrftoken')`.
 * - Awaits and processes the JSON response from the server.
 * - If the response is not OK, it displays an alert with the error message.
 * - If successful, it toggles the `liked` class on the button and switches the icon:
 *   - From filled heart (`ri-heart-fill`) to outline (`ri-heart-line`) when unliking.
 *   - From outline to filled when liking.
 * - Displays a success/failure message depending on the action performed.
 */
async function formButtonLikedProducts(button, productId) {
    try {
        const response = await fetch('/favorites-products/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),  // CSRF token for security (Django context)
            },
            body: JSON.stringify({ product_id: productId }),
        });

        const data = await response.json();  // Parse JSON response

        if (!response.ok) {
            // Server responded with an error status
            openAlert(data.detail, 'red', 1500);
            return;
        }

        // Toggle the 'liked' state visually
        const isLiked = button.classList.contains("liked");
        const icon = button.querySelector('i');

        if (isLiked) {
            button.classList.remove("liked");
            icon.classList.replace("ri-heart-fill", "ri-heart-line");
            openAlert('Producto eliminado como Favorito.', 'red', 1500);
        } else {
            button.classList.add("liked");
            icon.classList.replace("ri-heart-line", "ri-heart-fill");
            openAlert('Producto agregado como Favorito!', 'green', 1500);
        }

    } catch (error) {
        console.error('Error:', error);  // Network error or unexpected exception
    }
};


/**
 * Attaches a click event listener to a "Like" button for a product.
 * @param {HTMLElement} button - The button element used to like a product.
 */
function btnLikeProductEvent(button) {
    button.addEventListener('click', function() {
        if (AUTH_STATUS) {
            const productId = button.getAttribute("data-index");
            formButtonLikedProducts(button, productId);
        } else {
            openAlert('Debe logearse para guardar en Favoritos.', 'red', 2500);
        }
    });
};


/**
 * Attaches a submit event to a form for adding a product to the shopping cart.
 * 
 * @param {HTMLFormElement} form - The form element used to submit the add-to-cart action.
 * @param {number} value - (Optional) The quantity of the product to add (default is 1).
 * 
 * Behavior:
 * - Prevents the default form submission.
 * - Retrieves the product ID from the form's related button's `data-index` attribute.
 * - Calls `handleCartActions` with the product ID, the action type `'add'`, and the quantity.
 */
function formToAddProducts(form, value = 1) {
    form.addEventListener("submit", async function (event) {
        event.preventDefault(); 
        
        const productId = form.getAttribute("data-index");
        handleCartActions(productId, 'add', value); 
    });
};


/**
 * Adds a click event listener to an image container element.
 * @param {HTMLElement} image - The clickable image container element.
 */
function imageContainerClickEvent(image) {
    image.addEventListener('click', function () {
        const url = this.getAttribute('data-url');
        window.location.href = url;
    });
};


/**
 * Initializes and opens a product modal when the related button is clicked.
 * 
 * @param {HTMLElement} overlay - The overlay element that dims the background when the modal is open.
 * @param {HTMLElement} button - The button that triggers the modal opening. Must have a `data-modal-id` attribute.
 * 
 * Behavior:
 * - Retrieves the modal ID from the button's `data-modal-id` attribute.
 * - Selects the modal element by ID and passes it to `setupToggleableElement`
 *   for handling open/close behavior.
 */
function openProductModal(overlay, button) {
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
};
