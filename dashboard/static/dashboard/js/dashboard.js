

/// <reference path="../../../../home/static/home/js/base.js" />
/// <reference path="../../../../dashboard/static/dashboard/js/dash_products.js" />


// ==============================================================
//      FORM GENERICO PARA UPDATEAR SECTIONS EN EL DASHBOARD modalFormEditModel
// ==============================================================
/**
 * Validates and sanitizes the product form data before sending it to the server.
 * This function checks the validity of numerical fields, sanitizes the product description to prevent XSS, 
 * and returns an object with the validated data or null if validation fails.
 *
 * @param {FormData} formData - The FormData object containing the form fields and their values.
 * @returns {Object|null} - Returns the validated data as an object, or null if validation fails.
 */
function validFormProduct(form, formData) {

    // 1. Validates if the value is a valid numeric string (only digits).
    function validNumeric(value) {
        if (/^\d+$/.test(value)) return value;  // Return the value if it's valid
        return null;  // Return null if it's not a valid numeric value
    }
    
    // 2. Validates if the value is a valid decimal format (allows digits, commas, and periods).
    // Ideal for validating prices for DRF.
    function validPrice(value) {
        if (/^[\d.,]+$/.test(value)) return value;  // Return the value if it's a valid decimal format
        return null;  // Return null if it's not a valid price format
    }

    // 3. Sanitizes the product description to prevent XSS (cross-site scripting) attacks.
    const sanitizedDescription  = DOMPurify.sanitize(form.querySelector('.description-preview').innerHTML);

    // 4. Custom validation rules for specific fields in the form.
    const dataToCheck = {
        'price': [validPrice(formData.get('price')), "El precio debe contener solo números, comas o puntos."],
        'stock': [validNumeric(formData.get('stock')), "El stock debe ser un número entero."],
        'discount': [validNumeric(formData.get('discount')), "El descuento debe ser un número entero."],
    };

    // 5. Evaluate validation errors.
    // Loop through the dataToCheck object to check if any field is invalid.
    for (const key in dataToCheck) {
        if (dataToCheck[key][0] == null) {
            openAlert(dataToCheck[key][1]);  // Show alert with the corresponding error message
            return null;  // Return null if there's an error, preventing the form from being sent
        }
    }

    // 6. Construct the final data object to be sent.
    const dataSend = {
        id: formData.get('id'),
        name: formData.get('name'),
        price: dataToCheck.price[0],    // Access the validated price value
        stock: dataToCheck.stock[0],    // Access the validated stock value
        discount: dataToCheck.discount[0],  // Access the validated discount value
        available: formData.get('available') === 'on',    // Convert 'on' value to boolean
        description: sanitizedDescription,  // Sanitized description to prevent XSS
        category: formData.get('category'),
        subcategory: formData.get('subcategory'),
        brand: formData.get('brand'),
        main_image: formData.get('main_image')
    };

    // For debugging: console.log("Datos a enviar:", JSON.stringify(dataSend, null, 2));
    return dataSend;  // Return the validated data object to be sent
}


/**
 * Sends a PUT request to update the product data using Fetch API.
 *
 * @param {HTMLFormElement} form - The form element containing the action URL.
 * @param {Object} dataSend - The validated product data to be sent as JSON.
 * @throws Will throw an error if the response status is not OK (non-2xx).
 */
async function updateProductData(form, dataSend) {
    const response = await fetch(form.action, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify(dataSend)
    });

    const data = await response.json();

    // If the response failed, notify the user and propagate the error to the caller
    if (!response.ok) {
        openAlert('Something went wrong while updating the product. Please reload the page.', 'red', 1500);
        // Esto propaga el error hacia el try/catch de la function anterior, lo cual es correcto (similar al raise Py).
        throw new Error(`API Error [${response.status}]: ${JSON.stringify(data)}`);
    }

    // If the request was successful, show confirmation to the user
    openAlert('Producto actualizado correctamente.', 'green', 1500);
}

/**
 * Sends a DELETE request to remove specific product images.
 *
 * @param {string} url - The endpoint URL for image deletion.
 * @param {number|string} product_id - The ID of the product associated with the images.
 * @param {Array<number|string>} imagesToDelete - An array of image IDs to be deleted.
 * @throws Will throw an error if the server responds with an error.
 */
async function deleteProductImages(url, product_id, imagesToDelete) {
    const response = await fetch(url, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            id: product_id,
            delete_images: imagesToDelete
        })
    });

    const data = await response.json();

    // If the server returns an error, propagate it to the caller
    if (!response.ok) {
        throw new Error(data.detail || 'Failed to delete images');
    }

    // On success, show confirmation message
    openAlert('Imágenes eliminadas correctamente', 'green', 1500);
}


/**
 * Sends a POST request to upload new product images using FormData.
 *
 * @param {string} url - The endpoint URL for image upload.
 * @param {number|string} product_id - The ID of the product to associate the images with.
 * @param {FileList|Array<File>} files - The list of image files to upload.
 * @throws Will throw an error if the server responds with an error.
 */
async function uploadProductImages(url, product_id, files) {
    const formData = new FormData();
    formData.append('id', product_id);
    Array.from(files).forEach( (file) => formData.append('images', file));

    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: formData
    });

    const data = await response.json();

    // If the server returns an error, propagate it to the caller
    if (!response.ok) {
        throw new Error(data.detail || 'Failed to upload images');
    }

    // On success, show confirmation message
    openAlert('Imágenes subidas correctamente.', 'green', 1500, true);
}


/**
 * Handles the submission of form data in a modal, including product data, image deletion, and image upload.
 * This function manages the UI, performs validation, and sends requests to the server for product updates and image management.
 *
 * @param {HTMLFormElement} form - The form element containing the product data and images.
 */
async function submitFormModalData(form) {
    const submitButton = form.querySelector('button[type="submit"]');
    const formData = new FormData(form);
    // formData.forEach((value, key) => { console.log(`${key}: ${value}`); });  // for debug

    try {
        // 1. Disable submit button and prevent clicking to show a loading state
        submitButton.disabled = true;
        document.body.style.pointerEvents = 'none';
        submitButton.innerHTML = `
            <i class="ri-loader-2-fill icon-small"></i>
            <b>Por favor espere...</b>
        `;

        // 2. Convert FormData to an object and validate specific values
        const dataSend = validFormProduct(form, formData);
        if (dataSend === null) return;     // Error in validation, alert already shown in process Form Product

        // 3. Update product data
        await updateProductData(form, dataSend);

        // 4. Gather checked checkboxes to delete images
        const checkboxes = form.querySelectorAll('input[name="delete_images"]:checked');
        const imagesToDelete = Array.from(checkboxes).map(checkbox => checkbox.value);
        console.log(imagesToDelete)

        // 5. Validate if there are images to delete
        if (imagesToDelete.length > 0) {
            // Fetch the URL for deleting images
            const deleteImgUrl = form.dataset.deleteImages;
            await deleteProductImages(deleteImgUrl, dataSend.id, imagesToDelete);
        }
        
        // 6. Upload new images if any are selected
        const imageInput = form.querySelector('.image-input');

        if (imageInput.files.length > 0) {
            const uploadImgsUrl = form.dataset.createImages; 
            await uploadProductImages(uploadImgsUrl, dataSend.id, imageInput.files);
        }

        // 7. Apply changes and update UI after successful submission
        submitButton.innerHTML = `
            <i class="ri-checkbox-circle-line icon-small"></i>
            <b>Cambios Guardados</b>
        `;

        setTimeout(() => {
            // 7.a. Close the modal after the changes are saved
            const btnCloseForm = form.querySelector('#form-modal-close');
            if (btnCloseForm) btnCloseForm.click();  // Trigger the close event
            
            // 7.b. Update the table via AJAX (search or filters)
            const hiddenSearchForm = document.getElementById('btn-search-dashboard');
            if (hiddenSearchForm) hiddenSearchForm.click();  // Trigger the update
            
        }, 800);  // Wait 800ms = 0.8 seconds to apply changes

    } catch (error) {
        // 8. Handle errors (network or JSON parsing errors)
        openAlert('Problema de conexión. Revise su red e intente nuevamente', 'red', 1500);
        console.error('Error:', error);

    } finally {
        // 9. Restore UI (always executed, regardless of try/error)
        document.body.style.pointerEvents = '';
        submitButton.disabled = false;
    }
}


/**
 * Dynamically updates a dashboard section by performing a GET request with form parameters,
 * then replacing the inner HTML of a target section with the fetched HTML content.
 * Also rebinds event listeners for interactive elements within the updated section.
 *
 * Requirements for the form:
 * - Must have an `action` attribute (URL endpoint).
 * - Must include a `data-table` attribute that corresponds to the section's ID to update.
 * - Must have standard input fields and a submit button (`<button type="submit">`).
 *
 * @param {HTMLFormElement} form - The form element used to build the query and determine which section to update.
 */
async function updateDashboardSection(form) {

    const formData = new FormData(form);
    const submitButton = form.querySelector('button[type="submit"]');

    try {
        // 1. Disable the submit button to prevent multiple submissions
        submitButton.disabled = true;

        // 2. Build the final URL using the form's action and serialized query parameters
        const url = form.action;
        const params = new URLSearchParams(formData).toString();
        const finalUrl = `${url}${url.includes('?') ? '&' : '?'}${params}`;

        // 3. Perform the GET request to fetch the updated HTML section
        const response = await fetch(finalUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // If the response fails, throw an error to be caught later
        if (!response.ok) throw new Error('Network response was not ok');

        // 4. Extract the JSON response (expected to include HTML string for the section)
        const data = await response.json();

        // 5. Replace the inner HTML of the section specified by the form's data-table attribute
        const dataTable = form.getAttribute('data-table');
        const tableSection = document.getElementById(dataTable);
        tableSection.innerHTML = data.html_section;

        // 6. Rebind all dynamic events for the updated section
        if (dataTable === 'table-products') {
            rowsProductsEvents(tableSection);     // For row click/modal functionality
            eventsTableProducts(tableSection);    // For forms and filters
        }

    } catch (error) {
        // Log any errors to the console for debugging
        console.error('Error:', error);
    } finally {
        // 7. Re-enable the submit button regardless of success or failure
        submitButton.disabled = false;
    }
}


/* =======================================================================
    DASHBOARD SIDEBAR STUFF
======================================================================= */
document.addEventListener("DOMContentLoaded", function () {

    // asignar eventos a la sidebar/dashboard
    const btnShowDashboard = document.getElementById("dashboard-show")
    const sideDashboard = document.getElementById("dashboard")
    
    btnShowDashboard.addEventListener("click", (event) => {
        event.stopPropagation();
        toggleState(sideDashboard)
    });
    
    sideDashboard.addEventListener("click", () => {
        toggleState(sideDashboard)
    });

    document.addEventListener("click", (event) => {
        // Si el dashboard está abierto
        if (sideDashboard.getAttribute('data-state') === 'open') {
            // Verifica si el clic NO fue dentro del dashboard
            if (!sideDashboard.contains(event.target) && event.target !== btnShowDashboard) {
                toggleState(sideDashboard);
            }
        }
    });
    
    // asignar eventos de mostrar a las secciones
    const buttons = document.querySelectorAll('.btn-dashboard');
    const sections = document.querySelectorAll('.dashboard-section');


    buttons.forEach( (button, index) => {
        button.addEventListener('click', (event) => {

            // no asigna evento al btnShowDashboard
            if (index == 0) return;    

            event.stopPropagation();

            const sectionId = button.getAttribute('data-section');
    
            if (sectionId) {
                // Oculta todas las secciones antes de mostrar la nueva
                sections.forEach(section => section.classList.remove('active'));
    
                // Muestra la sección correspondiente
                dashSection = document.getElementById(sectionId);
                dashSection.classList.add('active');

                eventsOnDashboard(sectionId, dashSection)
            }

            if (sideDashboard.getAttribute('data-state') === 'open') {
                toggleState(sideDashboard)
            }

            // Falta logica de eventos a asginar REMEMBER
        });
    });

    // this is for update some dashboard tab
    buttons[3].click()
});

/*
section id = string like 'products' 
dash section = html element
*/
function eventsOnDashboard(sectionId, dashSection) {

    if (sectionId == 'products') {

        formModalAddProduct(dashSection);
        formBtnSelectFilterEvents(dashSection);
        formArrowsSorted(dashSection);
        formInputSearchRealTime(dashSection);
        formResetFilters(dashSection);

        /* this events is for dynamic updates reasign events */
        const tableSection = dashSection.querySelector(`#table-${sectionId}`);
        rowsProductsEvents(tableSection);
        eventsTableProducts(tableSection);
    }
};
