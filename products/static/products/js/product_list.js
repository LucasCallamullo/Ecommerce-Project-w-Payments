

let make_filter = false;


// ==========================================================================
//         AJAX PARA LAS TARJETAS QUE SE PRESENTAN en el product_list
// ==========================================================================
function updateProductListFromInput() {
    // Recuperamos los filtros directamente desde el contenedor
    const filtersElement = document.getElementById('filters');
    const filters = filtersElement.dataset;
    
    const searchInput = document.getElementById('search-input');

    // Acceder a los filtros directamente (data-category-id --> categoryId, automático camelCase)
    // Se asignan valores por defecto en caso de no existir, utiles para la logica el '0'
    const categoryId = filters.categoryId || '';
    const subCategoryId = filters.subCategoryId || '';
    const topQuery = filters.topQuery || '';
    const inputNow = searchInput.value;

    // para los casos donde se quiera resetear el filtro
    if (make_filter && inputNow.length < 3) {
        make_filter = false
        updateProductList('0', topQuery, categoryId, subCategoryId);
        return;
    }

    // Verificar que la longitud del input sea >= 3 antes de continuar
    if (inputNow.length < 3) return;

    // timer de 300 ms para evitar multiples consultas 
    let debounceTimer;
    clearTimeout(debounceTimer);

    debounceTimer = setTimeout(function() {
        updateProductList(inputNow, topQuery, categoryId, subCategoryId);
        make_filter = true
    }, 300);
};


async function updateProductList(inputNow, topQuery, categoryId, subCategoryId) {
    try {
        const url = `/products-search/?inputNow=${encodeURIComponent(inputNow)}
        &topQuery=${encodeURIComponent(topQuery)}&categoryId=${encodeURIComponent(categoryId)}
        &subCategoryId=${encodeURIComponent(subCategoryId)}`.replace(/\s+/g, '');

        console.log('Request URL:', url); // Verifica la URL generada

        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) throw new Error('Network response was not ok');

        const data = await response.json();
        
        // realizar cambios en el contenedor y reasignar eventos 
        const carritoContent = document.getElementById('search-results');
        carritoContent.innerHTML = data.html_cards;
        productButtonEvents();

    } catch (error) {
        console.error('Error:', error);
    }
}


function productButtonEvents() {
    // Agregar el evento click dinámicamente
    document.querySelectorAll('.prod-add-button').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.getAttribute('data-product-id');
            handleCartActions(productId, 'add', 1); 
        });
    });

    // Detiene la propagación del evento hacia el <figure>
    document.addEventListener('DOMContentLoaded', () => {
        const buttons = document.querySelectorAll('.prod-add-button');
        buttons.forEach(button => {
            button.addEventListener('click', (event) => {
                event.stopPropagation(); 
                console.log(`Producto ID: ${button.dataset.productId}`);
            });
        });
    });
}


// llamado inicial para actualizar la pagina
productButtonEvents()

