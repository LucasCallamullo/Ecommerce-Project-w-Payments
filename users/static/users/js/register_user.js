

/// <reference path="../../../../home/static/home/js/base.js" />

document.addEventListener('DOMContentLoaded', () => {
    // FORM HANDLER INITIALIZATION
    // ----------------------------
    /**
     * Initializes form handling for the registration form.
     * Note: The handleFormActions function is imported from widget_register.js
     * which is preloaded earlier in base.html due to its script placement.
     */
    const form = document.getElementById('register-form');
    if (form) {
        handleFormActions(form, "Register");
    }

    // ACCOUNT BUTTON HANDLER
    const btnHaveAccount = document.getElementById('have-account');
    const userButtons = document.querySelectorAll('.user-button');

    if (btnHaveAccount && userButtons.length > 0) {
        btnHaveAccount.addEventListener('click', function(event) {
            /**
             * Determines which user button to click based on viewport width
             * @type {boolean} isDesktop - True if viewport is 992px or wider
             * @type {number} buttonIndex - Dynamic button index (0 for mobile, 1 for desktop)
             */
            const isDesktop = window.innerWidth >= 992;
            const buttonIndex = isDesktop ? 1 : 0;
            
            // Safely get the target button
            const userLoginButton = userButtons[buttonIndex];
            
            if (userLoginButton) {
                userLoginButton.click();
                // Prevent event bubbling to parent elements
                event.stopPropagation();
            }
        });
    }
});