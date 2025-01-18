

// ================================================================================
//                        Profile home Handle ajax 
// ================================================================================
function onloadEventsTabs(dataContent) {
    if (dataContent === "Second Tab") {
        assignButtonsAddCartFavs();
        initSwiper();
    }
}


document.addEventListener('DOMContentLoaded', function () {
    const menuItems = document.querySelectorAll('.cover-menu li a');
    const contentDivs = {
        'First Tab': document.getElementById('first-tab'),
        'Second Tab': document.getElementById('second-tab'),
        'Third Tab': document.getElementById('third-tab'),
    };

    menuItems.forEach(item => {
        item.addEventListener('click', async function (e) {
            e.preventDefault();

            // Quitar clase 'active' de todos los elementos
            menuItems.forEach(i => i.parentElement.classList.remove('active'));
            this.parentElement.classList.add('active');

            const dataContent = this.getAttribute('data-content');
            const contentDiv = contentDivs[dataContent];

            // Oculta otros tabs y muestra el actual
            Object.values(contentDivs).forEach(div => div.style.display = 'none');
            contentDiv.style.display = 'block';

            try {
                // Realiza la solicitud AJAX para cargar el contenido
                const response = await fetch(`/profile/${dataContent.toLowerCase().replace(' ', '-')}/`);
                const data = await response.json();
                
                // cargar los scripts propios del html que vienen desde la respuesta json
                data.scripts.forEach(scriptSrc => {

                    const script = document.createElement('script');
                    script.src = scriptSrc;
                    script.defer = true;
                    script.onload = () => onloadEventsTabs(dataContent);
                    document.body.appendChild(script);

                });

                // Inserta el contenido HTML en el div
                contentDiv.innerHTML = data.html;

            } catch (error) {
                console.error('Error loading content:', error);
                contentDiv.innerHTML = `<p>Error loading content.</p>`;
            }
        });
    });

    // Llama al clic del primer tab automáticamente al cargar la página
    const firstTab = menuItems[0];
    if (firstTab) {
        firstTab.click();
    }
});


