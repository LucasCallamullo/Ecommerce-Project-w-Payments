

/// <reference path="../../../../home/static/home/js/base.js" />



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
                document.getElementById(sectionId).classList.add('active');
            }

            if (sideDashboard.getAttribute('data-state') === 'open') {
                toggleState(sideDashboard)
            }
        });
    });


    buttons[3].click()

});

