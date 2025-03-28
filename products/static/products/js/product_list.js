

/// <reference path="../../../../home/static/home/js/base.js" />
/// <reference path="../../../../products/static/products/js/products_utils.js" />

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
        assignProductEvents();
            
    } catch (error) {
        console.error('Error:', error);
    }
}


// ==========================================================================
//        function to asign events
// ==========================================================================
function assignProductEvents() {
    document.querySelectorAll(".btn-like").forEach(button => {
        btnLikeProductEvent(button);
    });

    document.querySelectorAll('.prod-extender-btn').forEach(form => {
        formToAddProducts(form);
    });

    document.querySelectorAll('.image-container').forEach(image => {
        imageContainerClickEvent(image);
    });

    const overlay = document.getElementById('overlay-products-modal');
    document.querySelectorAll('.corner-box').forEach(button => {
        openProductModal(overlay, button)
    });
};

document.addEventListener('DOMContentLoaded', () => {
    assignProductEvents();
});



