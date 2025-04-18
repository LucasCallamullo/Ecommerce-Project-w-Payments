

/// <reference path="../../../../home/static/home/js/base.js" />

// ========================================================================
//                   Main Nav Fixed DESKTOP
// ========================================================================
let isMainNavFixed = false; // Flag to track the state of the navbar

document.addEventListener("DOMContentLoaded", function () {

    const header = document.querySelector("header");
    const nav = document.querySelector("#main-nav");
    const navList = document.querySelector("#main-nav-list");
    
    if ( !header || !nav || !navList ) return; // Prevent errors if elements don't exist

    const headerHeight = header.offsetHeight;
    
    const logoData = document.getElementById("logo-url");
    const logoUrl = logoData.getAttribute("data-img");
    const homeUrl = logoData.getAttribute("data-url");

    // Create the dynamic logo container
    const logoContainer = document.createElement("div");
    logoContainer.classList.add("logo-container-fixed");
    logoContainer.innerHTML = `
        <a href="${homeUrl}" class="w-100">
            <img src="${logoUrl}" class="logo" alt="logo">
        </a>
    `;

    function handleScroll() {
        if (window.scrollY > headerHeight && !isMainNavFixed) {
            // Add fixed navigation and logo
            if (!navList.querySelector(".logo-container-fixed")) {
                navList.insertBefore(logoContainer, navList.firstChild);
            }
            nav.classList.add("fixed-nav", "active");
            isMainNavFixed = true;

        } else if (window.scrollY <= headerHeight && isMainNavFixed) {
            // Remove fixed navigation and logo
            if (navList.contains(logoContainer)) {
                navList.removeChild(logoContainer);
            }
            nav.classList.remove("fixed-nav", "active");
            isMainNavFixed = false;
        }
    }

    // Only add the scroll event listener when needed
    window.addEventListener("scroll", handleScroll, { passive: true });
});



// ========================================================================
// Evento de anmimaciones en drop menu categories GENERAL DESKTOP AND MOBILE
// ========================================================================
document.addEventListener("DOMContentLoaded", function () {
    // Configuración para los dropdowns
    const dropdownBtns = document.querySelectorAll(".dropdown-btn");
    const dropdownMenus = document.querySelectorAll(".dropdown-menu");
    const arrowDrops = document.querySelectorAll(".arrow-drop"); // Seleccionar las flechas

    dropdownBtns.forEach((btn, index) => {
        const menu = dropdownMenus[index]; // Relacionar el botón con su menú
        const arrowDrop = arrowDrops[index]; // Relacionar el botón con su flecha

        // Configurar el comportamiento de "clic fuera"
        setupClickOutsideClose(btn, menu, (isExpanded) => {
            arrowDrop.classList.toggle("rotate", isExpanded); // Rotar la flecha
        });
    });
});


// ========================================================================
//             EVENTS FOR DROPDOWN SUB CONTENT
// ========================================================================
document.addEventListener("DOMContentLoaded", function() {

    const dropdownItems = document.querySelectorAll(".dropdown-item");

    let hideTimeout, showTimeout;
    let isSubMenuVisible = false;
    let flagOneTime = false;
    let sameDropdownItem = -1;

    const positionSubMenu = (item, subMenu, index) => {
        if ( !item || !subMenu ) return;

        const rect = item.getBoundingClientRect();
        const subMenuHeight = subMenu.offsetHeight;
        
        subMenu.style.visibility = "hidden";
        subMenu.style.position = "fixed";
        subMenu.style.left = `${rect.right}px`;
        subMenu.style.zIndex = "9999";

        if ( index >= 7 ) {
            subMenu.style.top = `${rect.bottom - subMenuHeight}px`;
            if ( !flagOneTime ) {
                flagOneTime = true
                positionSubMenu(item, subMenu, index);
            }
        } else {
            subMenu.style.top = `${rect.top}px`;
        }
        subMenu.style.visibility = "visible";
    }

    let mainNavCloseOneTime = false;
    // Function to handle scroll event only when submenu is visible
    const onScroll = (item, subMenu, index) => {
        if ( !isSubMenuVisible ) return;
        
        //conditions to hide submenu when switching from main navbar to fixed navbar
        if ( isMainNavFixed && !mainNavCloseOneTime ) {
            closeSubMenu(subMenu, index, 10);
            mainNavCloseOneTime = true;
        } else if ( !isMainNavFixed && mainNavCloseOneTime) {
            mainNavCloseOneTime = false;
        }

        window.requestAnimationFrame(() => positionSubMenu(item, subMenu, index));
    }
    
    const scrollListeners = new Map(); // Guardará las funciones de cada índice

    function showSubMenu(item, subMenu, index) {
        if ( isSubMenuVisible && sameDropdownItem != index ) closeSubMenu(subMenu, index, 10);
            
        clearTimeout(hideTimeout);
        sameDropdownItem = index;

        showTimeout = setTimeout(() => {
            subMenu.style.display = "block";
            positionSubMenu(item, subMenu, index);

            if (!isSubMenuVisible) {
                flagOneTime = false;
                isSubMenuVisible = true;
                activeSubMenuIndex = -1;

                // Crear función con los parámetros correctos
                const scrollHandler = (event) => onScroll(item, subMenu, index);
                scrollListeners.set(index, scrollHandler);

                window.addEventListener("scroll", scrollHandler);
            }
        }, 100);
    }

    function closeSubMenu(subMenu, index, timer) {
        clearTimeout(showTimeout);

        hideTimeout = setTimeout(() => {
            subMenu.style.display = "none";
            isSubMenuVisible = false;
            sameDropdownItem = -1;

            // Eliminar correctamente el evento scroll usando el Map
            if (scrollListeners.has(index)) {
                window.removeEventListener("scroll", scrollListeners.get(index));
                scrollListeners.delete(index);
            }
        }, timer);
    }

    dropdownItems.forEach((item, index) => {
        const subMenu = item.querySelector(".sub-dropdown-content");
        if (!item || !subMenu) return;

        subMenu.dataset.index = index;
        item.dataset.index = index;

        // Show submenu on hover
        item.addEventListener("mouseenter", () => {
            showSubMenu(item, subMenu, index);
        });
            
        item.addEventListener("mouseleave", () => {
            closeSubMenu(subMenu, index, 100);
        });

        // Hide submenu when leaving it
        subMenu.addEventListener("mouseleave", () => {
            if (sameDropdownItem == index) return;
            closeSubMenu(subMenu, index, 10);
        });
    });
});


// ========================================================================
//             MAIN NAV BAR MOBILE - MENU SHOW UTILS
// ========================================================================
document.addEventListener("DOMContentLoaded", function () {
    // This dict configure the events add and remove automatically
    setupToggleableElement({
        toggleButton: document.getElementById('nav-toggle'),
        closeButton: document.getElementById('menu-mobile-close'),
        element: document.getElementById('nav-menu-mobile'),
        overlay: document.getElementById('overlay-menu-mobile'),
    });
});


// ========================================================================
//             MAIN NAV BAR MOBILE - SEARCH BAR MOBILE UTILS
// ========================================================================
document.addEventListener("DOMContentLoaded", function () {
    const searchButton = document.getElementById('top-btn-search');
    const searchForm = document.getElementById('search-bar-mobile');
    const backButton = document.getElementById('back-search-form');


    /**
     * Closes the search form by toggling its visibility and updating the aria-expanded attribute.
     */
    function closeSearch() {
        toggleState(searchForm);
        const isExpanded = searchButton.getAttribute("aria-expanded") === "true";
        searchButton.setAttribute("aria-expanded", !isExpanded);
    }

    /**
     * Sets up the click-outside behavior for the search form.
     * When the search button is clicked, the form toggles visibility.
     * If the user clicks outside the form, it closes automatically.
     * Additionally, when the form is expanded, the back button can close it.
     */
    setupClickOutsideClose(searchButton, searchForm, (isExpanded) => {
        if (isExpanded) {
            // When the form is shown, enable the back button to close it
            backButton.addEventListener('click', closeSearch);
        } else {
            // When the form is hidden, remove the event to avoid unnecessary listeners
            backButton.removeEventListener('click', closeSearch);
        }
    });
});

