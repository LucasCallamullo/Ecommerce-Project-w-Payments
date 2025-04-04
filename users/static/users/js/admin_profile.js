

/// <reference path="../../../../home/static/home/js/base.js" />

// Configuraciones establecidas para el tercer tab
function formEditSubmit(form) {

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = form.querySelector('button[type="submit"]');
        submitBtn.disabled = true;  // Deshabilitar botón durante el envío
        
        try {
            // Convertimos FormData en JSON
            const formData = new FormData(form);
            const jsonData = Object.fromEntries(formData.entries());

            // Ajuste para select del form de users por role
            const role = form.querySelector("select[name='role']")
            if (role) {
                jsonData.role = role.value;
            }; 

            // Ajuste para checkboxes (ya que no se envían si están desmarcados)
            const checkbox = form.querySelector('[name="is_active"]');
            if (checkbox) {
                jsonData.is_active = checkbox.checked;
            }

            const response = await fetch(form.action, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(jsonData),
            });

            if (!response.ok) throw new Error('Error en la red');
            
            const data = await response.json();
            
            // Feedback visual al usuario
            openAlert(data.message || 'se realizaron cambios correctamente');
            
        } catch (error) {
            openAlert(error || 'Error al conectar con el servidor');
            console.error('Error:', error);
        } finally {
            submitBtn.disabled = false;
        }
    });
}


document.addEventListener('DOMContentLoaded', () => {

    const formsShipments = document.querySelectorAll('.shipment-grid');
    formsShipments.forEach((form) => {
        formEditSubmit(form);
    });

    const formsUserRoles = document.querySelectorAll(".user-role-form")
    formsUserRoles.forEach((formRole) => {
        formEditSubmit(formRole);
    });

    const formStore = document.getElementById('form-store-grid');
    formEditSubmit(formStore);
});



// Configuraciones establecidas para el primer tab
document.addEventListener('DOMContentLoaded', () => {

    // setear variables del form modal
    const imgBtns = document.querySelectorAll('.image-overlay');
    const modalForm = document.getElementById('upload-form');
    const modalClose = document.getElementById('upload-form-close');
    const overlay = document.getElementById('overlay-upload-form');
    
    // Changes en modal
    const modalImg = document.getElementById('img-modal');
    const spanTittles = document.querySelectorAll('.modal-object');

    // Inputs image forms modal
    const imageInput = document.getElementById("image-input");
    const imgPreview = document.getElementById('img-modal-new');      // Imagen de previsualización

    const mainCheck = document.getElementById('main-img-check');
    const mainTextCb = document.getElementById('main-img-text');

    const hiddenCheck = document.getElementById('img-hidden-check');
    const hiddenTextCb = document.getElementById('img-hidden-text');


    // Declara variables en un ámbito superior
    let currentIndexHeader, currentObjectName;

    // para guardar los estados del modal
    let initialState = {};

    function saveInitialState() {
        initialState = {
            image: null, // No se puede leer el archivo directamente, se comparará después
            mainCheck: mainCheck.checked,
            hiddenCheck: hiddenCheck.checked,
        };
    }

    function hasChanged() {
        return (
            mainCheck.checked !== initialState.mainCheck ||
            hiddenCheck.checked !== initialState.hiddenCheck ||
            imageInput.files.length > 0 // Se ha subido una nueva imagen
        );
    }

    function modalFormImages(imgBtns) {
        imgBtns.forEach((imgBtn) => {
            setupToggleableElement({
                toggleButton: imgBtn,
                closeButton: modalClose,
                element: modalForm,
                overlay: overlay,
                onOpenCallback: () => {
                    let imageUrl = imgBtn.getAttribute('data-img');
                    let mainImg = imgBtn.getAttribute('data-main');
                    let hiddenImg = imgBtn.getAttribute('data-hidden');

                    // Guarda en variables globales
                    currentIndexHeader = imgBtn.getAttribute('data-index');
                    currentObjectName = imgBtn.getAttribute('data-object');

                    modalImg.src = imageUrl; // Asigna la imagen solo si existe
                    modalImg.alt = "Preview Image"; // Opcional: cambia el `alt` también

                    // Limpiar el input file completamente
                    imageInput.value = '';
                    imgPreview.src = ''; 

                    // Verifica si el header es la imagen principal y actualiza el checkbox
                    if (mainImg === 'True') {
                        mainCheck.checked = true;
                        mainTextCb.textContent = "Sí";
                    } else {
                        mainCheck.checked = false;
                        mainTextCb.textContent = "No";
                    }

                    // Verifica si el header esta oculto y actualiza el checkbox
                    if (hiddenImg === 'True') {
                        hiddenCheck.checked = true;
                        hiddenTextCb.textContent = "Sí";
                    } else {
                        hiddenCheck.checked = false;
                        hiddenTextCb.textContent = "No";
                    }

                    // Modifica cada titulo segun el nombre del componente
                    spanTittles.forEach((spanTit) => {
                        spanTit.textContent = currentObjectName
                    });

                    // Guardar el estado inicial cuando se abra el modal
                    saveInitialState();
                }
            });
        });
    }
    // debemos asignar este evento minimo en este punto
    modalFormImages(imgBtns);
    
    // Mantiene actualizado el texto cuando el usuario cambia el checkbox
    mainCheck.addEventListener('change', () => {
        mainTextCb.textContent = mainCheck.checked ? "Sí" : "No";
    });

    // Mantiene actualizado el texto cuando el usuario cambia el checkbox
    hiddenCheck.addEventListener('change', () => {
        hiddenTextCb.textContent = hiddenCheck.checked ? "Sí" : "No";
    });

    const modalCheckDel = document.getElementById('check-delete');
    const contCheckDel = document.getElementById('cont-delete-btn');
    modalCheckDel.addEventListener('change', () => {
        let isOpen = toggleState(contCheckDel)
        if (isOpen) {
            scrollToSection(contCheckDel)
        }
    });

    // Captura evento del modal
    // const modalForm = document.getElementById('upload-form');
    modalForm.onsubmit = async function(event) {
        event.preventDefault();

        if (!hasChanged()) {
            openAlert("No se han realizado cambios.");
            return;
        }

        const clickedButton = event.submitter; // Botón que disparó el envío
        const action = clickedButton.value; // "edit" o "delete"
        
        let formData = new FormData();
        if (imageInput.files.length > 0) {
            formData.append("image", imageInput.files[0]);
        }
        formData.append("main_image", mainCheck.checked);
        formData.append("soft_delete", hiddenCheck.checked);
        formData.append("action_name", action);
        formData.append("obj_id", currentIndexHeader);
        formData.append("obj_name", currentObjectName);

        try {
            const response = await fetch("/upload-to-imgbb/", {
                method: "POST",
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: formData
            });

            if (!response.ok) throw new Error("HTTP error " + response.status);
            
            const data = await response.json();

            switch(data.action) {  // Más limpio que múltiples if-else
                case 'create':
                    openAlert("Registro creado exitosamente.", 'green', 1500);
                    break;
                case 'update':
                    openAlert("Registro actualizado.", 'green', 1500);
                    break;
                case 'delete':
                    openAlert("Registro eliminado.", 'red', 1500);
                    break;
                default:
                    console.warn("Operación desconocida:", data.action);
            }
            
            // cambiar contenido con ajax
            const firstTab = document.getElementById('first-tab')
            firstTab.innerHTML = data.tab_html

            // cerrar el modal actual
            modalClose.click();

            // reasignar eventos
            const imgBtns = document.querySelectorAll('.image-overlay');
            modalFormImages(imgBtns);

            console.log("Success:", data);

        } catch (error) {
            console.error("Error:", error);
            openAlert(error || "Error al procesar la solicitud");
        }
    };

    // Agregar evento de mostrar la imagen nueva para que el usuario vea por cual va a reemplazar
    imageInput.addEventListener('change', function(event) {
        const file = event.target.files[0]; // Obtener el archivo seleccionado
        if (file) {
            const reader = new FileReader();
    
            reader.onload = function(e) {
                imgPreview.src = e.target.result; // Asignar la imagen cargada
            };
    
            reader.readAsDataURL(file); // Leer el archivo como URL
        }
    });
});

// Selecciona los enlaces de las pestañas
// Selecciona las secciones de contenido
document.addEventListener("DOMContentLoaded", function () {
    const tabs = document.querySelectorAll(".cover-menu li a"); 
    const contents = document.querySelectorAll(".tab-content"); 

    tabs.forEach(tab => {
        tab.addEventListener("click", function () {
            const target = this.getAttribute("data-content");

            // Remueve la clase 'active' de todas las pestañas
            tabs.forEach(t => t.parentElement.classList.remove("active"));

            // Agrega la clase 'active' a la pestaña seleccionada
            this.parentElement.classList.add("active");

            // Oculta todos los contenidos
            contents.forEach(content => content.setAttribute('data-state', 'closed'));

            // Muestra el contenido correspondiente
            const tab = document.getElementById(target)
            toggleState(tab)
        });
    });

    // Mostrar la primera pestaña por defecto
    // document.querySelector(".cover-menu li a").click();
    tabs[1].click();
});