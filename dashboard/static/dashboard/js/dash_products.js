

/// <reference path="../../../../home/static/home/js/base.js" />
/*
INDICE
    Initializes the "Add Product" modal functionality
    Manages subcategory selection logic
    form-reset-filters
    Initializes real-time search functionality within a given dashboard section
    Initializes filter button and form interactions
    Handles table sorting functionality
    Manages main image selection in a product gallery
    Initializes modal form events with proper cleanup
    Manages description modal events with custom markdown processing
*/


/**
 * Initializes a Choices.js instance on a select element, ensuring that
 * any previous instance is properly destroyed to prevent duplicates or memory leaks.
 *
 * @param {HTMLElement} element - The <select> element to enhance with Choices.js
 */
function initSelectChoices(element) {
    // If a previous Choices instance exists on the element, destroy it to prevent conflicts
    if (element.choicesInstance) element.choicesInstance.destroy();

    // Create and assign a new Choices.js instance to the element
    element.choicesInstance = new Choices(element, {
        searchEnabled: true,      // Enable search functionality inside the select dropdown
        itemSelectText: '',       // Removes the default "Press to select" text
        shouldSort: false         // Keep the original order of the options (no automatic sorting)
    });
}


/* =======================================================================
    FORMS DASH SECTION THAT IT S NOT CHANGES IN SECTION PRODCUTS
======================================================================= */
/**
 * Initializes the "Add Product" modal functionality:
 * 1. Gets all required DOM elements
 * 2. Sets up toggle behavior using a reusable component
 * 
 * @param {HTMLElement} dashSection - Container element holding modal components
 */
function formModalAddProduct(dashSection) {
    // 1. DOM element selection
    const btnAddProduct = dashSection.querySelector('#add-new-product');
    const formAddProduct = dashSection.querySelector('#form-new-product');
    const btnCloseForm = dashSection.querySelector('#form-new-product-close');
    const overlay = dashSection.querySelector('#overlay-new-product');

    // 2. Modal configuration
    setupToggleableElement({
        toggleButton: btnAddProduct,  // Main trigger button
        closeButton: btnCloseForm,    // Close button inside modal
        element: formAddProduct,      // Modal form element
        overlay: overlay,             // Background overlay
        onOpenCallback: () => {       // Optional open event handler
            console.log('Modal opened for new product');

            // a) Set initial form events (e.g., submission or validation)
            formModalStartEvents(formAddProduct, btnCloseForm);

            // b) Set selects Choices for brands and categories
            const categorySelect = formAddProduct.querySelector('.category-select');
            const brandSelect = formAddProduct.querySelector('.brand-select');
            initSelectChoices(categorySelect);
            initSelectChoices(brandSelect);

            // c) Set up dynamic subcategory logic (e.g., dependent dropdowns)
            subcategorySelectEvents(formAddProduct, true);

            // d) Load and set the product description dynamically into the modal
            descriptionModalEvents(formAddProduct);
        }
    });
}


/**
 * Attaches submit event handlers to all forms with the class 'form-reset-filters'
 * within the specified dashboard section. These forms are typically used to reset filters.
 *
 * @param {HTMLElement} dashSection - The container that holds the reset filter forms.
 */
function formResetFilters(dashSection) {
    const formsReset = dashSection.querySelectorAll('.form-reset-filters');
    
    formsReset.forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault(); // Prevent the default form submission

            const submitButton = form.querySelector('button[type="submit"]');
            
            // Trigger the dashboard update with the current form
            updateDashboardSection(form);

            // Add a visual indicator (CSS class) to the submit button
            if (submitButton) {
                submitButton.classList.add('active-main');

                // Remove the class after 2 seconds to reset the visual feedback
                setTimeout(() => {
                    submitButton.classList.remove('active-main');
                }, 2000);
            }
        });
    });
}



/**
 * Manages subcategory selection logic by:
 * 1. Handling category change events
 * 2. Syncing subcategory selections to hidden input
 * 3. Dynamically showing relevant subcategory selects
 * 
 * @param {HTMLElement} form - The parent form element
 * @param {boolean} [choicesInit=false] - Whether to initialize Choices.js
 */
function subcategorySelectEvents(form, choicesInit = false) {
    // 1. Configure category selection handler
    const categorySelect = form.querySelector('.category-select');
    categorySelect.addEventListener('change', (e) => {
        openSelectByCategory(e.target.value); // Update UI based on selection
    });

    // 2. Sync subcategory selections to hidden input
    const subcatInput = form.querySelector('.selected-subcategory');
    const subcatSelects = form.querySelectorAll('.subcat-select');
    subcatSelects.forEach(select => {
        select.addEventListener('change', (e) => {
            subcatInput.value = e.target.value; // Store selected value
        });
    });

    // 3. Manage subcategory visibility
    const subcatContainers = form.querySelectorAll('.subcat-container');
    function openSelectByCategory(categorySelected) {
        // 3.1 Hide all subcategory containers initially
        subcatContainers.forEach(container => {
            container.setAttribute('data-state', 'closed');
        });
        
        // 3.2 Reset and validate selection
        subcatInput.value = '0'; // Default value
        if (categorySelected === '0' || !categorySelected) return;

        // 3.3 Show relevant subcategory container
        const subcatContainer = form.querySelector(`.subcat-cont-${categorySelected}`);
        if (!subcatContainer) return;
        
        toggleState(subcatContainer); // Show container

        // 3.4 Initialize enhanced select if needed
        const subcatSelect = subcatContainer.querySelector('.subcat-select');
        if (subcatSelect) {
            subcatInput.value = subcatSelect.value; // Sync initial value

            // 3.5 Only creates choices instance if the flag is active
            if (choicesInit) initSelectChoices(subcatSelect);
        }
    };

    // Initialize with default category
    openSelectByCategory(categorySelect.value);
};


/**
 * Initializes real-time search functionality within a given dashboard section.
 *
 * Features implemented:
 * 1. Debounced Input Handling
 *    - Avoids excessive form submissions by delaying the trigger until the user has paused typing.
 * 
 * 2. Form Submission Control
 *    - Prevents default form submission and instead triggers a custom handler to update the UI dynamically.
 * 
 * 3. Dynamic Filter Transfer 
 *    - Ensures that additional filters (e.g., category, subcategory, availability) are copied from a hidden form
 *      and included in the active search query.
 *
 * @param {HTMLElement} dashSection - The parent container element that includes the search form and filters.
 */
function formInputSearchRealTime(dashSection) {
    const DEBOUNCE_DELAY = 500; // Delay (in milliseconds) before triggering search
    const MIN_CHARS = 2;        // Minimum number of characters required to trigger a search

    // Cache key DOM elements
    const formInputDash = dashSection.querySelector('#search-dashboard');          // Main visible search form
    const hiddenFiltersForm = dashSection.querySelector('#form-hidden-filters');   // Hidden form containing filter values
    const searchInput = formInputDash?.querySelector('input[name="query"]');       // Text input field for search queries
    const searchBtn = formInputDash?.querySelector('#btn-search-dashboard');       // Optional search button for manual triggering

    // Exit early if essential elements are missing
    if (!formInputDash || !searchInput) return;

    let debounceTimer = null;     // Timer reference for debouncing
    let isFilterActive = false;   // Flag to track whether search is actively filtering results

    /**
     * Handles form submission by injecting query and filters into the visible form,
     * then programmatically triggering a submit action.
     *
     * @param {string} query - The search query to submit (defaults to empty string)
     */
    function submitSearch(query = '') {
        // 1. Update the search input value before submitting
        formInputDash.query.value = query;

        // 3. Transfer relevant filter fields from the hidden form to the visible form
        if (hiddenFiltersForm) {
            const fieldsToTransfer = ['category', 'subcategory', 'available'];
            fieldsToTransfer.forEach(field => {
                const source = hiddenFiltersForm.querySelector(`[name="${field}"]`);
                const target = formInputDash.querySelector(`[name="${field}"]`);
                if (source && target) target.value = source.value;
            });
        }

        // 2. Programmatically submit the form to trigger UI update
        formInputDash.querySelector('[type="submit"]').click();
    }

    /**
     * Custom form submission event handler
     * Prevents default form reload and instead performs an AJAX-like update.
     */
    formInputDash.addEventListener('submit', (event) => {
        event.preventDefault();
        updateDashboardSection(formInputDash); // Custom function to refresh the dashboard content
    });

    /**
     * Handles input events on the search field.
     * - Debounces input to limit request rate.
     * - Triggers reset or search depending on input length.
     */
    searchInput.addEventListener('input', () => {
        const query = searchInput.value.trim();

        // Reset search if query becomes too short and a filter was previously active
        if (isFilterActive && query.length < MIN_CHARS) {
            isFilterActive = false;
            submitSearch('');
            return;
        }

        // Do not trigger search for short queries
        if (query.length < MIN_CHARS) return;

        // 1. Debounce logic: delay execution until user stops typing
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            isFilterActive = true;
            submitSearch(query);
        }, DEBOUNCE_DELAY);
    });

    /**
     * Optional manual search trigger using a button
     */
    searchBtn?.addEventListener('click', () => {
        submitSearch(searchInput.value.trim());
    });
}


/**
 * Initializes filter button and form interactions by:
 * 1. Setting up form submission handling
 * 2. Configuring click-outside close behavior
 * 3. Initializing subcategory selection events
 * 
 * @param {HTMLElement} dashSection - Container element holding filter components
 */
function formBtnSelectFilterEvents(dashSection) {

    const btnFilter = dashSection.querySelector('#btn-filter');
    const formFilter = dashSection.querySelector('#form-select-filters');

    // 1. Configure form submission
    formFilter.addEventListener("submit", (event) => {
        event.preventDefault();
        updateDashboardSection(formFilter, 'form-select-filters');
    });

    // 2. Set up dropdown behavior
    setupClickOutsideClose(btnFilter, formFilter, (isOpen) => {
        // 2.1 Toggle visual active state
        btnFilter.classList.toggle('active-main', isOpen);
    });

    // 3. Initialize subcategory selection handlers
    subcategorySelectEvents(formFilter);
};


/**
 * Handles table sorting functionality by:
 * 1. Locating all sort buttons in a dashboard section
 * 2. Initializing base table functionality
 * 3. Attaching click handlers to each sort button
 *    - Toggles sort direction (asc/desc)
 *    - Updates hidden form values
 *    - Triggers form submission
 * 
 * @param {HTMLElement} dashSection - Parent element containing sort buttons
 */
function formArrowsSorted(dashSection) {
    // 1. Get all sort buttons in the container
    const btnSorts = dashSection.querySelectorAll('.btn-sorted');

    // 2. Configure click handlers for each sort button
    btnSorts.forEach((btn) => {
        btn.addEventListener('click', () => {
            // 3.1 Extract current sort parameters
            const sortBy = btn.getAttribute('data-sort-by');
            const dataSorted = btn.getAttribute('data-sorted');
    
            // 3.2 Reverse sort direction
            const sorted = (dataSorted === 'asc') ? 'desc' : 'asc';
            btn.setAttribute('data-sorted', sorted);
    
            // 3.3 Refresh form references (post-DOM update)
            let formAllFilters = dashSection.querySelector('#form-hidden-filters');
            let btnAllFilters = formAllFilters.querySelector('[type="submit"]');
            
            // 3.4 Update form values
            formAllFilters.sort_by.value = sortBy;
            formAllFilters.sorted.value = sorted;
    
            // 3.5 Trigger data refresh
            btnAllFilters.click();
        });
    });
};


/**
 * Manages main image selection in a product gallery by:
 * 1. Setting up event delegation for image selection
 * 2. Applying visual indicators to the selected main image
 * 3. Maintaining state through data attributes
 * 
 * @param {HTMLElement} modalForm - The container element for product images
 */
function changeMainImageEvent(modalForm) {
    // 1. Get image container and setup event delegation
    const imageContainer = modalForm.querySelector('#modal-images-cont');

    // 2. Handle change events from radio inputs
    imageContainer.addEventListener('change', function(e) {
        // 2.1 Only process events from our target checkboxes
        if (!e.target.classList.contains('check-main')) return;

        // 3. Get selected image ID
        const selectedId = e.target.value;

        // 4. Process all images in container
        const allImages = this.querySelectorAll('img');
        allImages.forEach(img => {
            const imgId = img.dataset.index;

            // 4.1 Apply visual and data state to selected image
            if (imgId === selectedId) {
                img.classList.add('border-main');
                img.dataset.main = "true";
            } 
            // 4.2 Remove indicators from other images
            else {
                img.classList.remove('border-main');
                img.dataset.main = "false";
            }
        });
    });
}


/**
 * Initializes modal form events with proper cleanup:
 * 1. Image preview handling
 * 2. Click-outside closing
 * 3. Modal cancel button
 * 
 * This use eventHandlersMap for delete correctly some events
 * @param {HTMLElement} modalForm - The modal form container
 * @param {HTMLElement} modalClose - The close button modal form
 */
function formModalStartEvents(modalForm, modalClose) {
    // 1. IMAGE PREVIEW HANDLING
    const imageInput = modalForm.querySelector('.image-input');
    const imgPreview = modalForm.querySelector('.new-image');

    // Clean previous image handlers
    if (eventHandlersMap.has(imageInput)) {
        const prevHandler = eventHandlersMap.get(imageInput);
        imageInput.removeEventListener('change', prevHandler);
    }

    // Reset and setup new handler
    imageInput.value = '';
    imgPreview.src = '';
    
    const imageHandler = (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => imgPreview.src = e.target.result;
            reader.readAsDataURL(file);
        }
    };
    
    imageInput.addEventListener('change', imageHandler);
    eventHandlersMap.set(imageInput, imageHandler);

    // 2. MODAL CLOSING HANDLERS
    const cancelModal = modalForm.querySelector('.form-modal-cancel');
    
    // Clean previous cancel handlers
    if (eventHandlersMap.has(cancelModal)) {
        const prevHandler = eventHandlersMap.get(cancelModal);
        cancelModal.removeEventListener('click', prevHandler);
    }

    // Setup new cancel handler
    const closeHandler = () => modalClose.click();
    cancelModal.addEventListener('click', closeHandler);
    eventHandlersMap.set(cancelModal, closeHandler);
}


// ==============================================================
//      MODAL FORM TO UPDATE SOME MODEL
// ==============================================================
/* los parametros son una fila de la tabla y el form Modal que se abre */
function updateModalFormInputs(row, modalForm) {

    // 1. Parseamos el json asociado al atributo data-model esta es la mejor forma para recuperar
    // desde nuestro template donde usamos el filtro |escape_data, para traernos los str ya formateados
    const dataset = JSON.parse(row.getAttribute('data-model'));    // getAttribute es mejor que .dataset.model);

    const contImages = modalForm.querySelector('#modal-images-cont');
    contImages.innerHTML = ''    

    // En este caso el return dentro del forEach funciona igual que un continue en un for
    Object.entries(dataset).forEach(([key, value]) => {

        if (key.startsWith("image-")) {
            // obtenemos atributos desde la key
            const [, isMain, imageId] = key.split("-");
        
            const imageHTML = `
                <div class="d-flex-col w-100 gap-1">
                    <img 
                        src="${value}" 
                        alt="Product image" 
                        data-index="${imageId}" 
                        data-main="${isMain}"
                        class="${isMain === "True" ? 'border-main' : ''}"
                    />
                    
                    <div class="container-space-evenly gap-1">
                        <label class="d-flex gap-1">
                            <input 
                                type="radio"
                                class="check-main"
                                name="main_image"
                                value="${imageId}" 
                                ${isMain === "True" ? "checked" : ""}
                            >
                            <span>Principal</span>
                        </label>

                        <label class="d-flex gap-1">
                            <input type="checkbox" name="delete_images" value="${imageId}">
                            <span>Eliminar</span>
                        </label>
                    </div>
                </div>
            `;
        
            contImages.insertAdjacentHTML('beforeend', imageHTML);
            return;
        }

        // Buscar input con id="modal-[key]"
        const input = modalForm.querySelector(`#modal-${key}`);

        // Si no existe el input o no es un campo editable, saltearlo
        if (!input || input.disabled) return;

        // Si es input, textarea o select, cambiar su value
        if (input.tagName == "INPUT" ) {
            if (input.type === "checkbox") {
                input.checked = value === "True";
            } else {
                input.value = value;
            }
        }

        // Destruye el anterior choice.js y lo recrea por cada vez que se abre el modal
        else if (input.tagName == "SELECT") {
            input.value = value;    // asigna su value al elemento
            initSelectChoices(input);
        }

        // esto es solo para cambiar algunos titulos
        else if (["SPAN", "P", "B"].includes(input.tagName)) {
            input.textContent = value;
        }
    });
}


/**
 * Manages description modal events with custom markdown processing:
 * 1. Converts HTML to custom markdown syntax
 * 2. Provides real-time preview with custom formatting
 * 3. Handles bidirectional conversion between HTML and custom markdown
 * 
 * @param {HTMLElement} modalForm - Container element holding modal components
 * @param {string|null} productId - ID of the product being edited
 */
function descriptionModalEvents(modalForm, productId = null, tableSection = null) {
    /**
     * Converts textarea content to formatted HTML preview
     * @param {HTMLTextAreaElement} textarea - Input element with raw text
     * @param {HTMLElement} preview - Container for rendered preview
     */
    function updatePreview(textarea, preview) {
        const text = textarea.value;
        const lines = text.split('\n');
        let htmlOutput = '';

        lines.forEach(line => {
            let processedLine = line
                .replace(/\(\*\)/g, '<strong>(*)</strong>')  // Highlight (*) notation
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')  // Bold text
                .replace(/^\*-\s?(.*)/, '• $1')  // Small bullet point
                .replace(/^\*\s?(.*)/, '● $1')   // Normal bullet point
                .replace(/^--$/, '&nbsp;');  // Empty line placeholder

            htmlOutput += `<p>${processedLine}</p>`;
        });

        preview.innerHTML = htmlOutput;
    }

    /**
     * Converts HTML back to custom markdown syntax
     * @param {string} html - HTML string to convert
     * @returns {string} Custom markdown formatted text
     */
    function htmlToCustomMarkdown(html) {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, 'text/html');
        const paragraphs = doc.querySelectorAll('p');
        let markdownOutput = '';

        paragraphs.forEach(p => {
            let line = p.innerHTML;

            // Processing order matters for nested formats
            line = line.replace(/<strong>\(\*\)<\/strong>/g, '(*)')
                       .replace(/<strong>(.*?)<\/strong>/g, '**$1**');

            // Handle bullet points
            if (line.startsWith('● ')) {
                line = '* ' + line.slice(2).trim();
            } else if (line.startsWith('• ')) {
                line = '*- ' + line.slice(2).trim();
            }

            // Handle empty lines
            if (line.includes('&nbsp;')) {
                line = '--';
            }

            markdownOutput += line + '\n';
        });

        return markdownOutput.trim();
    }

    // 1. DOM element initialization
    const textarea = modalForm.querySelector('.modal-description');
    const preview = modalForm.querySelector('.description-preview');

    // 2. Initial content conversion
    if (productId && tableSection) {
        const htmlString = tableSection.querySelector(`#template-${productId}`).innerHTML;
        textarea.value = htmlToCustomMarkdown(htmlString);
        updatePreview(textarea, preview);
    }

    // 3. Real-time preview with debounce
    let timeout;
    textarea.addEventListener('input', () => {
        clearTimeout(timeout);
        timeout = setTimeout(() => updatePreview(textarea, preview), 200);
    });
}


/* ======================================================================================
    Table section parameter indica que son funciones reasignadas post get, post, put 
====================================================================================== */
/**
 * Reassigns dynamic event listeners to form elements and filters inside the given table section.
 * This is necessary after re-rendering or dynamically updating a section in the dashboard,
 * ensuring all relevant forms continue functioning correctly.
 *
 * @param {HTMLElement} tableSection - The section of the dashboard containing the products table and related forms.
 */
function eventsTableProducts(tableSection) {

    // Reassign submit event to the hidden filters form after the section is re-rendered.
    const formAllFilters = tableSection.querySelector('#form-hidden-filters');
    if (formAllFilters) {
        formAllFilters.addEventListener('submit', (event) => {
            event.preventDefault(); // Prevent default form submission
            updateDashboardSection(formAllFilters); // Handle the filter logic via AJAX or similar
        });
    }

    // Reassign submit event to the modal form used to edit product data
    const formTableModal = tableSection.querySelector('#form-modal-table');
    if (formTableModal) {
        formTableModal.addEventListener('submit', async (e) => {
            e.preventDefault(); // Prevent full page reload
            await submitFormModalData(formTableModal); // Submit modal form data using custom async handler
        });
    }

    // If the dashboard has filters applied, generate a human-readable summary
    const filtersDiv = document.getElementById('filters-str');
    if (filtersDiv) {
        // Create an array of filter descriptions only if they are present
        const resumen = [
            filtersDiv.dataset.category && `Categoría: ${filtersDiv.dataset.category}`,
            filtersDiv.dataset.subcategory && `Subcategoría: ${filtersDiv.dataset.subcategory}`,
            filtersDiv.dataset.query && `Buscador: ${filtersDiv.dataset.query}`,
        ]
        .filter(Boolean) // Remove any falsy values
        .join(" | ");    // Join the valid filters with a pipe separator
        
        // Update the DOM with the filters summary, or a default message
        document.getElementById("resume-filters").textContent = resumen || "Sin filtros aplicados.";
    }
}


/**
 * Sets up dynamic form events for each row in the table section.
 * This function binds a modal form to each table row, allowing users to edit or view details
 * when a row is clicked. It initializes form behavior, image handling, and subcategory interactions.
 *
 * @param {HTMLElement} tableSection - The parent container that includes table rows and the modal elements.
 */
function rowsProductsEvents(tableSection) {
    // 1. Select all the necessary elements from the table section
    const rowsTable = tableSection.querySelectorAll('.row-table');         // All rows that should trigger the modal
    const modalForm = tableSection.querySelector('#form-modal-table');     // The modal form that opens on row click
    const modalClose = tableSection.querySelector('#form-modal-close');    // Button to close the modal
    const overlay = tableSection.querySelector('#overlay-table');          // Background overlay for the modal

    // 2. Iterate over each row to attach the event
    rowsTable.forEach((row) => {
        // Set up the toggleable modal behavior for the row
        setupToggleableElement({
            toggleButton: row,         // The row will act as the button to open the modal
            closeButton: modalClose,   // Modal close button
            element: modalForm,        // The modal form itself
            overlay: overlay,          // The overlay that darkens the background
            onOpenCallback: () => {    // Callback when the modal opens

                // a) Set initial form events (e.g., submission or validation)
                formModalStartEvents(modalForm, modalClose);

                // b) Attach main image change event handler
                changeMainImageEvent(modalForm);

                // c) Update the form inputs based on the selected row's data
                updateModalFormInputs(row, modalForm);

                // d) Set up dynamic subcategory logic (e.g., dependent dropdowns)
                subcategorySelectEvents(modalForm, true);

                // e) Load and set the product description dynamically into the modal
                const productId = row.getAttribute('data-index');
                descriptionModalEvents(modalForm, productId, tableSection);
            }
        });
    });
}
