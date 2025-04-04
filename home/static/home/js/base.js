

// Esto lo podés poner al final de tu archivo JS, o en un <script> después de cargar la página
function forceReload() {
    const url = new URL(window.location.href);
    url.searchParams.set('v', Date.now()); // Crea un parámetro único cada vez
    window.location.href = url.toString();
};


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

        // Desactiva el botón "Back to Top" si está visible
        const backToTopBtn = document.getElementById("backToTop");
        toggleBackToTopButton(false, backToTopBtn);
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
 * Sets up a toggleable UI element (such as a modal or mobile menu) with automatic event management.
 * 
 * Example usage:
 * setupToggleableElement({
 *     toggleButton: document.getElementById('nav-toggle'),
 *     closeButton: document.getElementById('nav-close'),
 *     element: document.getElementById('nav-menu-mobile'),
 *     overlay: document.getElementById('overlay-menu-mobile'),
 *     onOpenCallback: () => console.log('Menu opened!') // Optional callback function
 * });
 * 
 * @param {Object} options - Configuration options for the toggleable element.
 * @param {HTMLElement} options.toggleButton - The button that opens the element.
 * @param {HTMLElement} options.closeButton - The button that closes the element.
 * @param {HTMLElement} options.element - The element to be shown/hidden (e.g., a modal or menu).
 * @param {HTMLElement} options.overlay - The overlay displayed behind the element.
 * @param {boolean} [options.flagStop=false] - Optional flag to stop event propagation when opening (default is false).
 * @param {Function} [options.onOpenCallback=null] - Optional function to execute when the element is opened.
 */
function setupToggleableElement(options) {
    const { toggleButton, closeButton, element, overlay, flagStop = false, onOpenCallback = null } = options;

    // Basic validation to ensure all required elements are present
    if (!toggleButton || !closeButton || !element || !overlay) {
        console.log('Some of the elements are missing.');
        return;
    }

    /**
     * Closes the toggleable element and overlay.
     * Also removes the click event listener from the close button to prevent memory leaks.
     * 
     * @param {Function} closeHandler - The function to remove from the close button's click event.
     */
    function closeElement(closeHandler) {
        toggleState(element);       // Hide the element (toggle class or visibility)
        closeOverlay(overlay);     // Hide the overlay

        if (closeButton && closeHandler) {
            closeButton.removeEventListener('click', closeHandler); // Clean up event listener
        }
    }

    /**
     * Opens the toggleable element and sets up necessary event listeners for closing.
     * Also manages event propagation if flagStop is enabled.
     * 
     * @param {Event} event - The click event from the toggle button.
     */
    function openElement(event) {
        if (flagStop) {
            event.stopPropagation(); // Prevent event bubbling if specified
        }

        toggleState(element); // Show the element

        if (typeof onOpenCallback === 'function') {
            onOpenCallback(); // Ejecuta la función pasada como parámetro si existe
        }

        // Define the handler for closing, which is self-removing
        const closeHandler = () => closeElement(closeHandler);
        closeButton.addEventListener('click', closeHandler); // Listen for close button click

        // Show the overlay and allow closing by clicking outside the element
        openOverlay(overlay, closeOverlayOnClick(element, closeButton, closeHandler));
    }

    // Attach click event to toggle button to open the element
    toggleButton.addEventListener('click', openElement);
}


/* ==========================================================================================
                Generic function to close elements by clicking outside them
========================================================================================== */
// Map to store close events for each trigger element
const closeEventsMap = new Map();

/**
 * Sets up a click-outside close behavior for a given trigger and target element.
 * When the trigger element is clicked, the target element toggles its visibility.
 * If the user clicks outside the target element, it will close automatically.
 *
 * @param {HTMLElement} triggerElement - The element that triggers the toggle (e.g., a button).
 * @param {HTMLElement} targetElement - The element to be shown/hidden (e.g., a dropdown menu).
 * @param {Function} [onToggle=() => {}] - Optional callback to execute when the target element toggles.
 */
function setupClickOutsideClose(triggerElement, targetElement, onToggle = () => {}) {
    /**
     * Handles the common logic for toggling the target element's state and managing close events.
     *
     * @param {boolean} isExpanded - The current expanded state of the target element.
     */
    function handleElement(isExpanded) {
        toggleState(targetElement);
        triggerElement.setAttribute("aria-expanded", !isExpanded);

        // Execute the optional callback with the new state
        onToggle(!isExpanded);

        if (!isExpanded) {
            // Add the close event to the map and document
            closeEventsMap.set(triggerElement, closeIfClickOutside);
            document.addEventListener("click", closeIfClickOutside);
        } else {
            // Remove the close event from the map and document
            document.removeEventListener("click", closeEventsMap.get(triggerElement));
            closeEventsMap.delete(triggerElement);
        }
    }

    /**
     * Handles the click-outside event to close the target element if the click occurs outside.
     *
     * @param {MouseEvent} event - The click event object.
     */
    function closeIfClickOutside(event) {
        const isExpanded = triggerElement.getAttribute("aria-expanded") === "true";
        if (!isExpanded) return;

        // If the click is outside the trigger and target elements, close the target element
        if (!triggerElement.contains(event.target) && !targetElement.contains(event.target)) {
            handleElement(isExpanded);
        }
    }

    /**
     * Handles the click event on the trigger element to toggle the target element's state.
     */
    function handleExpanded() {
        const isExpanded = triggerElement.getAttribute("aria-expanded") === "true";
        handleElement(isExpanded);
    }

    triggerElement.addEventListener("click", handleExpanded);
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

    const alertsContainer = document.getElementById('alerts-container');
    // Open the door! open the container
    if (alertsContainer.getAttribute('data-state') === 'closed') {
        alertsContainer.setAttribute('data-state', 'open');
    }

    // Determine the icon class based on the color
    const iconClass = color === 'red' ? 'ri-close-circle-line' : 'ri-checkbox-circle-line';

    // Create a new alert box element
    const alertBox = document.createElement('div');
    alertBox.classList.add('cont-custom-alert');
    alertBox.innerHTML = `
        <div class="container-space-between">
            <button class="btn">
                <i class="${iconClass} icon-medium"></i>
            </button>
            <span>${message}</span>
            <button class="btn">
                <i class="ri-close-circle-line icon-medium"></i>
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

    alertsContainer.appendChild(alertBox);
    alertBox.classList.add('show');

    // Function to check if the alerts container is empty and close it if needed
    const checkAndCloseContainer = () => {
        // If there are no more alert elements inside the container
        if (alertsContainer.children.length === 0) {
            alertsContainer.setAttribute('data-state', 'closed');
        }
    };

    // Remove the alert after timeout period and check container state
    setTimeout(() => {
        alertBox.remove();
        checkAndCloseContainer();
    }, timeout);

    // Add click event listeners to all close buttons in this alert
    const closeButtons = alertBox.querySelectorAll('button');
    closeButtons.forEach(button => {
        button.addEventListener('click', () => {
            alertBox.remove();
            checkAndCloseContainer();
        });
    });
}


// ========================================================================
//                   Dark Mode Event Listener
// ========================================================================
document.addEventListener('DOMContentLoaded', () => {
    // Get all theme toggle buttons and icons
    const themeToggleButtons = document.querySelectorAll('.theme-toggle');
    const themeIcons = document.querySelectorAll('.theme-icon');
    const htmlElement = document.documentElement;

    /**
     * Sets the theme and updates the UI
     * @param {string} theme - 'auto', 'light', or 'dark'
     */
    function setTheme(theme) {
        // Remove all theme classes first
        htmlElement.classList.remove('light-mode', 'dark-mode');
        
        if (theme === 'auto') {
            // Rely on system preference (no class added)
            localStorage.removeItem('themePreference');
        } else {
            // Apply manual theme class
            htmlElement.classList.add(`${theme}-mode`);
            localStorage.setItem('themePreference', theme);
        }
        
        // Update the icons to reflect current theme
        updateThemeIcons(theme);
    }

    /**
     * Updates the theme icons based on current theme
     * @param {string} theme - Current theme mode
     */
    function updateThemeIcons(theme) {
        // Determine if we're in dark mode (either manually or via system)
        const isDark = theme === 'dark' || 
                      (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches);
        
        // Toggle between moon (light) and contrast (dark) icons
        themeIcons.forEach(icon => {
            icon.classList.toggle('ri-moon-line', !isDark);
            icon.classList.toggle('ri-contrast-2-line', isDark);
        });
    }

    // Initialize theme from localStorage or use 'auto'
    const savedTheme = localStorage.getItem('themePreference') || 'auto';
    setTheme(savedTheme);

    /**
     * Cycles through theme options: auto → light → dark → auto...
     */
    function cycleTheme() {
        const currentPreference = localStorage.getItem('themePreference') || 'auto';
    
        // Orden de ciclo: auto -> light -> dark -> light
        const nextTheme = currentPreference === 'auto' ? 'light'
                        : currentPreference === 'light' ? 'dark'
                        : 'light';
    
        setTheme(nextTheme);
    }
    
    // Add click handlers to all toggle buttons
    themeToggleButtons.forEach(button => {
        button.addEventListener('click', cycleTheme);
    });

    // Listen for system theme changes (optional)
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        // Only update if we're in auto mode
        if (!localStorage.getItem('themePreference')) {
            updateThemeIcons('auto');
        }
    });
});



// ========================================================================
//                   Button back to the top 
// ========================================================================
let isBackToTopEventAdded = false; // Controla si el evento de clic está agregado

/**
 * Smoothly scrolls the page back to the top.
 */
function backToTheTop() {
    window.scrollTo({ top: 0, behavior: "smooth" });
}

/**
 * Muestra u oculta el botón "Back to Top" y agrega/remueve el evento de clic.
 */
function toggleBackToTopButton(show, backToTopBtn) {
    if (show) {
        backToTopBtn.classList.add("show");
        if (!isBackToTopEventAdded) {
            backToTopBtn.addEventListener("click", backToTheTop);
            isBackToTopEventAdded = true;
        }
    } else {
        backToTopBtn.classList.remove("show");
        if (isBackToTopEventAdded) {
            backToTopBtn.removeEventListener("click", backToTheTop);
            isBackToTopEventAdded = false;
        }
    }

    backToTopBtn.style.pointerEvents = show ? "all" : "none";
}

document.addEventListener('DOMContentLoaded', () => {
    const backToTopBtn = document.getElementById("backToTop");
    const progressCircle = backToTopBtn.querySelector(".progress circle");

    /**
     * Handles the scroll event to show or hide the button
     * and update the progress indicator circle.
     */
    window.addEventListener("scroll", function () {

        // Oculta el botón si el overlay está abierto
        if (overlayClickListener) {
            toggleBackToTopButton(false, backToTopBtn); 
            return;
        }
        
        let scrollTop = window.scrollY || document.documentElement.scrollTop; // Current scroll position
        let scrollHeight = document.documentElement.scrollHeight - window.innerHeight; // Total scrollable height
        let progress = (scrollTop / scrollHeight) * 100; // Calculates the scroll percentage

        // Show or hide the button based on scroll position
        toggleBackToTopButton(scrollTop > 100, backToTopBtn);
        
        // Adjust the progress circle stroke based on the scroll percentage
        // you must change values in base.html too for apply changes
        let dashOffset = 126 - (progress / 100) * 126; // 126 is the full circumference of the circle
        progressCircle.style.strokeDashoffset = dashOffset;
    }, { passive: true });
});


/**
 * Retrieves the value of a specified cookie by its name, commonly used for CSRF tokens.
 * 
 * @param {string} name - The name of the cookie whose value is to be retrieved.
 * @returns {string|null} The value of the cookie if found, otherwise null.
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Checks if the cookie has the desired name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                // Extracts and decodes the cookie value
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


/**
 * Formats a number by adding dots as thousand separators.
 * 
 * @param {number|string} number - The number to be formatted (can be an integer, float, or string).
 * @returns {string} The formatted number as a string with dots as thousand separators.
 */
function formatNumberWithPoints(number) {
    // If the value is null, undefined, or an empty string, return a blank space
    if (number === null || number === undefined || number === "") return " ";

    // Convert the string value to a number
    const price = parseFloat(number);
    
    // Check if the price is 0
    if (price === 0) return 'Gratis';

    // If the number is an integer, format it with thousand separators using dots
    if (Number.isInteger(price)) return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");

    // If the number has decimals, format it by separating thousands with dots and decimals with a comma
    let [integerPart, decimalPart] = price.toString().split(".");
    integerPart = integerPart.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    
    return decimalPart ? `${integerPart},${decimalPart}` : integerPart;
}


/**
 * Smoothly scrolls to a section with temporary visual highlight
 * @param {HTMLElement} section - DOM element to scroll to
 * @param {string} [color='red'] - Border highlight color (default: red)
 * @returns {void}
 */
function scrollToSection(section, color = 'red') {
    if (!section) return; // Basic null check
    
    // Scroll with offset managed via CSS (scroll-margin-top)
    section.scrollIntoView({ 
        behavior: 'smooth', 
        block: 'start' 
    });
    
    // Temporary highlight effect (2 seconds)
    section.style.boxShadow = `0 0 0 2px ${color}`;
    setTimeout(() => section.style.boxShadow = '', 2000);
}


/**
 * Displays error messages from a form submission.
 * 
 * This function iterates over an object containing form field errors and 
 * displays them as alerts with a red color. Each field may have multiple 
 * error messages associated with it.
 *
 * @param {Object} errors - An object where each key is a field name and 
 *                          its value is an array of error messages.
 * @param {number} [delay=2500] - The time in milliseconds before each alert disappears.
 */
function showErrorAlerts(errors, delay = 2500) {
    // Iterate over each field in the errors object
    for (let field in errors) {
        // Ensure the field actually belongs to the object (not from prototype)
        if (errors.hasOwnProperty(field)) {
            // Iterate over each error message for the given field
            errors[field].forEach((error) => {
                // Display an alert with the field name and its corresponding error message
                openAlert(`${field}: ${error}`, "red", delay);
            });
        }
    }
}



// ========================================================================
//                  Whatsap button
// ========================================================================
// Función para limpiar el número de teléfono y devolver la URL de WhatsApp
function formatPhoneNumber(cellphone) {
    // Elimina todos los caracteres no numéricos (como espacios, paréntesis, guiones)
    const formattedNumber = cellphone.replace(/[^\d]/g, '');
    // Si el número está bien formateado (empezando con un 9, después 11 dígitos)
    // Si el número está bien formateado (empezando con un 9, después 11 dígitos)
    if (formattedNumber.length < 6) {
        console.error("Número de teléfono no válido");
        return null;
    }

    return `https://wa.me/${formattedNumber}`;
}

// Wait until the DOM is fully loaded before executing the script
document.addEventListener('DOMContentLoaded', function() {
    // Get references to the DOM elements
    const floatingButton = document.getElementById('floating-wsp-btn');
    const floatingMenu = document.getElementById('floating-wsp-menu');
    const icon = floatingButton.querySelector('[data-icon]');

    // Initial configuration
    floatingButton.dataset.state = 'inactive'; // Set initial state
    const iconActive = floatingButton.dataset.iconActive; // Get active icon class from data attribute
    const iconInactive = floatingButton.dataset.iconInactive; // Get inactive icon class from data attribute

    /**
     * Toggles the button state between active and inactive
     * - Changes the data-state attribute
     * - Animates the icon change
     * - Shows/hides the floating menu
     */
    function toggleButtonState() {
        // Check current state
        const isActive = floatingButton.dataset.state === 'active';
        
        // Update state (toggle between active/inactive)
        floatingButton.dataset.state = isActive ? 'inactive' : 'active';
        
        // Change icon halfway through the animation (after 200ms)
        setTimeout(() => {
            // Switch between active/inactive icon classes
            icon.className = isActive ? iconActive : iconInactive;
            icon.classList.add('icon-xl');
        }, 200);
        
        // Toggle menu visibility (show when becoming active, hide when becoming inactive)
        floatingMenu.classList.toggle('show', !isActive);
    }

    // Event listeners

    // Handle click on the floating button
    floatingButton.addEventListener('click', function(e) {
        e.stopPropagation(); // Prevent event from bubbling up
        toggleButtonState(); // Toggle the button state
    });

    // Manejar clics dentro del menú flotante para que no se cierre
    floatingMenu.addEventListener('click', function(event) {
        event.stopPropagation(); // Evita que el clic en el menú lo cierre
    });

    // Handle clicks anywhere in the document
    document.addEventListener('click', function() {
        // If menu is currently shown, close it
        if (floatingMenu.classList.contains('show')) {
            toggleButtonState();
        }
    });

    // Assign href generic to btn-wsp
    const productLink = document.getElementById('wsp-link');
    const cellphone = productLink.getAttribute('data-wsp');
    const whatsappUrl = formatPhoneNumber(cellphone);

    // Crea el mensaje dinámicamente con los valores del producto
    const message = `Buenos días, Quería consultar sobre formas de pago con tarjeta en el local?`;

    // Si el número es válido, concatenamos la URL con el mensaje
    if (whatsappUrl) {
        const finalWhatsappUrl = `${whatsappUrl}?text=${encodeURIComponent(message)}`;
        productLink.setAttribute('href', finalWhatsappUrl);
    }
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