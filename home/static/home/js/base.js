

/**
 * `AUTH_STATUS` is defined as a boolean by evaluating `isAuthenticated`.  
 * This will serve as a global variable to check if the user is authenticated.
 */
const isAuthenticated = document.getElementById('auth-status').getAttribute('data-register-user');
const AUTH_STATUS = isAuthenticated === 'true'; 


/**
 * Defined in static/home/js/base.js
 * Toggles the state of an element/component between 'open' and 'closed'
 * based on its current state, and triggers associated animations.
 * @param {HTMLElement} element - The element whose state is being toggled.
 * @returns {boolean} - Returns a boolean indicating the new state (true if opened, false if closed).
 */
function toggleState(element) {
    const isOpen = element.getAttribute('data-state') === 'open';
    element.setAttribute('data-state', isOpen ? 'closed' : 'open');
    return !isOpen;
}


// ============================================================================
//                Overlay functions and events
// ============================================================================
let overlayClickListener = null;  // Holds the current click listener for the overlay

/**
 * Opens the overlay and adds the event listener for click events.
 * @param {HTMLElement} overlay - The overlay element to open.
 * @param {Function} eventFunction - The function to execute when the overlay is clicked.
 * This function toggles the 'show' class to display the overlay and assigns a click event listener if not already assigned.
 */
function openOverlay(overlay, eventFunction) {
    overlay.classList.add('show');

    if (!overlayClickListener) {
        overlayClickListener = eventFunction;
        overlay.addEventListener('click', overlayClickListener); 
    }

    const backToTopBtn = document.getElementById("backToTop");
    if (backToTopBtn) {
        backToTopBtn.classList.remove("show");
    }
}

/**
 * Closes the overlay and removes the event listener for click events.
 * @param {HTMLElement} overlay - The overlay element to close.
 * This function removes the 'show' class to hide the overlay and removes the click event listener.
 */
function closeOverlay(overlay) {
    overlay.classList.remove('show');
    
    if (overlayClickListener) {
        overlay.removeEventListener('click', overlayClickListener);  
        overlayClickListener = null; 
    }
}

/**
 * Generates a click event handler to close the overlay when clicked.
 * @param {HTMLElement} element - The element whose state is toggled when the overlay is clicked.
 * @param {HTMLElement} buttonClose - The button to close the modal.
 * @param {Function} closeHandler - The function to remove the event listener from the button.
 * @returns {Function} - The event handler function that will close the overlay on click.
 */
function closeOverlayOnClick(element, buttonClose=null, closeHandler=null) {
    return function (e) {
        if (e.target === this) {
            console.log('Overlay clicked');
            closeOverlay(this); 
            toggleState(element);

            // Elimina el event listener del botón de cerrar
            if (buttonClose && closeHandler) {
                console.log('Se borró correctamente el evento del botón de cierre');
                buttonClose.removeEventListener('click', closeHandler);
            }
        }
    };
}


/**
 * Configura un elemento que se puede abrir y cerrar (como un modal o menú).
 * || Defined in static/home/js/base.js
 * @param {Object} options - Opciones para configurar el elemento.
 * @param {HTMLElement} options.toggleButton - Botón que abre el elemento.
 * @param {HTMLElement} options.closeButton - Botón que cierra el elemento.
 * @param {HTMLElement} options.element - El elemento que se abre y cierra (modal o menú).
 * @param {HTMLElement} options.overlay - El overlay que se muestra detrás del elemento.
 */
function setupToggleableElement(options) {
    const { toggleButton, closeButton, element, overlay } = options;

    if (!toggleButton || !closeButton || !element || !overlay) return;

    // Función para cerrar el elemento
    function closeElement(closeHandler) {
        toggleState(element);
        closeOverlay(overlay);

        // Elimina el event listener del botón de cerrar
        if (closeButton && closeHandler) {
            closeButton.removeEventListener('click', closeHandler);
        }
    }

    // Función para abrir el elemento
    function openElement(event) {
        event.stopPropagation(); // Evita que el evento se propague al contenedor
        toggleState(element);

        // Define el manejador de eventos para cerrar el elemento
        const closeHandler = () => closeElement(closeHandler);
        closeButton.addEventListener('click', closeHandler);

        // Abre el overlay
        openOverlay(overlay, closeOverlayOnClick(element, closeButton, closeHandler));
    }

    // Evento de clic en el botón de abrir
    toggleButton.addEventListener('click', openElement);
}


/* ==========================================================================================
                Generic Function for Show and Hide Alerts Events
========================================================================================== */
/**
 * Displays a custom alert message on the screen.
 * 
 * This function creates a new alert box dynamically and adds it to the alerts container.
 * The alert can be customized with a message, a predefined color, and a timeout duration.
 * It also includes a close button for manual dismissal.
 * 
 * @param {string} message - The text message to display in the alert.
 * @param {string} [color='green'] - The color of the alert.
 * @param {number} [timeout=1000] - The duration (in ms) before the alert is automatically removed.
 */
function openAlert(message, color = 'green', timeout = 1000) {
    // Determine the icon class based on the color
    const iconClass = color === 'red' ? 'ri-close-circle-line' : 'ri-checkbox-circle-line';

    // Create a new alert box element
    const alertBox = document.createElement('div');
    alertBox.classList.add('cont-custom-alert');
    alertBox.innerHTML = `
        <div class="d-flex gap-4">
            <button class="btn">
                <i class="${iconClass}"></i>
            </button>
            <span>${message}</span>
            <button class="btn">
                <i class="ri-close-circle-line"></i>
            </button>
        </div>
    `;

    // Predefined color mapping
    const colorMap = {
        green: "#00c01a",
        red: "#be0404e3",
        blue: "#0000ff",
        yellow: "#ffff00"
    };

    if (colorMap[color]) {
        color = colorMap[color];
    }
    alertBox.style.color = color;
    alertBox.style.backgroundColor = color;

    const alertsContainer = document.getElementById('alerts-container');
    alertsContainer.appendChild(alertBox);
    alertBox.classList.add('show');

    // Automatically remove the alert after the specified timeout
    setTimeout(() => alertBox.remove(), timeout);

    // Add event listener to close buttons inside the alert
    const closeButtons = alertBox.querySelectorAll('button');
    closeButtons.forEach(button => {
        button.addEventListener('click', () => alertBox.remove());
    });
}


// ========================================================================
//                   Dark Mode Event Listener
// ========================================================================
document.addEventListener('DOMContentLoaded', function () {
    const themeToggleButtons = document.querySelectorAll('.theme-toggle');
    const themeIcons = document.querySelectorAll('.theme-icon');
    
    /**
     * Updates the theme icons based on the current theme state.
     * @param {boolean} isDarkMode - Indicates whether dark mode is enabled.
     */
    function updateThemeIcons(isDarkMode) {
        themeIcons.forEach(icon => {
            icon.classList.toggle('ri-moon-line', !isDarkMode);
            icon.classList.toggle('ri-contrast-2-line', isDarkMode);
        });
    }
    
    /**
     * Toggles dark mode and updates the icons accordingly.
     */
    function toggleTheme() {
        const isDarkMode = document.body.classList.toggle('dark-mode');
    
        updateThemeIcons(isDarkMode);
        // Store the new theme state in localStorage only if it has changed
        if (localStorage.getItem('darkMode') !== String(isDarkMode)) {
            localStorage.setItem('darkMode', isDarkMode);
        }
    }
    
    // Attach event listeners to all theme toggle buttons
    themeToggleButtons.forEach(button => {
        button.addEventListener('click', toggleTheme);
    });

    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    document.body.classList.toggle('dark-mode', isDarkMode);
    updateThemeIcons(isDarkMode);
});


// ========================================================================
//                   Button back to the top 
// ========================================================================
document.addEventListener("DOMContentLoaded", function () {
    const backToTopBtn = document.getElementById("backToTop");
    const progressCircle = backToTopBtn.querySelector(".progress circle");

    let flag_control = false; // Flag to control the addition/removal of the click event

    /**
     * Smoothly scrolls the page back to the top.
     */
    function backToTheTop() {
        window.scrollTo({ top: 0, behavior: "smooth" });
    }

    /**
     * Handles the scroll event to show or hide the button
     * and update the progress indicator circle.
     */
    window.addEventListener("scroll", function () {
        let scrollTop = window.scrollY || document.documentElement.scrollTop; // Current scroll position
        let scrollHeight = document.documentElement.scrollHeight - window.innerHeight; // Total scrollable height
        let progress = (scrollTop / scrollHeight) * 100; // Calculates the scroll percentage

        // Show or hide the button based on scroll position
        if (scrollTop > 100) {
            if (!flag_control) {
                backToTopBtn.classList.add("show"); // Show the button
                backToTopBtn.addEventListener("click", backToTheTop); // Add the click event
                flag_control = true; // Mark that the event has been added
            }
        } else {
            if (flag_control) {
                backToTopBtn.classList.remove("show"); // Hide the button
                backToTopBtn.removeEventListener("click", backToTheTop); // Remove the click event
                flag_control = false; // Mark that the event has been removed
            }
        }

        // Adjust the progress circle stroke based on the scroll percentage
        let dashOffset = 126 - (progress / 100) * 126; // 126 is the full circumference of the circle
        progressCircle.style.strokeDashoffset = dashOffset;
    });
});



/*
// Get the device state from the meta tag
put this <meta id="device-meta" data-state="desktop"> in html in a "head"

const deviceMeta = document.getElementById("device-meta");
const updateDeviceState = () => {
    const isMobile = window.innerWidth <= 768;
    deviceMeta.setAttribute("data-state", isMobile ? "mobile" : "desktop");
};

updateDeviceState(); // Set initial state

window.addEventListener("resize", updateDeviceState);



and included this verification in the functions in the future
document.addEventListener("DOMContentLoaded", function () {
    // Prevent unnecessary content loading on mobile, as this listener is only needed for desktop
    const deviceState = deviceMeta.getAttribute("data-state");
    if (deviceState === "mobile") return;

    // resto del codigo
}
*/