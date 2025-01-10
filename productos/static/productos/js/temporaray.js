
    // Funcion simple de incremento y decremento
    function increment(button) {
    const input = button.parentElement.querySelector('.quantity-input-2');
    let value = parseInt(input.value);
    input.value = value + 1;
    }

    function decrement(button) {
        const input = button.parentElement.querySelector('.quantity-input-2');
        let value = parseInt(input.value);
        if (value > 1) {
            input.value = value - 1;
        }
    }

    // Añade un evento de clic a cada botón que interactúe con la cantidad
    $(document).on('click', '[id^="add-to-cart2-"]', function() {
        const productoId = $(this).attr('id').split('-').pop(); // Captura el ID del producto desde el ID del botón
        const quantity = document.getElementById(`quant-cart-${productoId}`).value; // Captura el valor actual de la cantidad
        handleActions(productoId, 'add', quantity); // Llama a la función para manejar la acción
    });


    window.onload = () => {
        const previewEl = document.querySelector('.prod-image-preview');
        const previewWidth = previewEl.offsetWidth;
        const previewHeight = previewEl.offsetHeight;

        // Set background images for thumbnails based on their data attributes
        const thumbnails = document.querySelectorAll('.prod-small-image');
        thumbnails.forEach(thumbnail => {
            const imgUrl = thumbnail.dataset.imageUrl;
            thumbnail.style.backgroundImage = `url(${imgUrl})`;
        });

        // Set default active thumbnail and preview image
        const defaultThumbnail = document.querySelector('.prod-small-image[data-index="1"]');
        if (defaultThumbnail) {
            defaultThumbnail.classList.add('active');
            const defaultImageUrl = defaultThumbnail.dataset.imageUrl;
            previewEl.style.backgroundImage = `url(${defaultImageUrl})`;
        }

        // Update the preview image on thumbnail mouseover
        document.querySelector('.prod-left-column').addEventListener('mouseover', e => {
            if (e.target.classList.contains('prod-small-image')) {
                const imgUrl = e.target.dataset.imageUrl;
                previewEl.style.backgroundImage = `url(${imgUrl})`;
            }
        });

        // Change the active thumbnail and update the preview image on thumbnail click
        document.querySelector('.prod-left-column').addEventListener('click', e => {
            if (e.target.classList.contains('prod-small-image') && !e.target.classList.contains('active')) {
                document.querySelector('.prod-small-image.active').classList.remove('active');
                e.target.classList.add('active');
                const imgUrl = e.target.dataset.imageUrl;
                previewEl.style.backgroundImage = `url(${imgUrl})`;
            }
        });

        // Handle zoom effect on mouse move when the preview is zoomed
        previewEl.addEventListener('mousemove', e => {
            if (previewEl.classList.contains('prod-zoomed')) {
                const offsetXPercent = Math.round(e.offsetX * 100 / previewWidth);
                const offsetYPercent = Math.round(e.offsetY * 100 / previewHeight);
                previewEl.style.backgroundPosition = `${offsetXPercent}% ${offsetYPercent}%`;
            }
        });

        // Reset background position when the mouse leaves the preview
        previewEl.addEventListener('mouseleave', e => {
            previewEl.style.removeProperty('background-position');
        });

        // Toggle zoom mode on preview click
        previewEl.addEventListener('click', () => {
            if (previewEl.classList.contains('prod-zoomed')) {
                previewEl.classList.remove('prod-zoomed');
                previewEl.classList.add('prod-normal');
                previewEl.style.backgroundSize = 'cover';
                previewEl.classList.add('prod-zoom-in-cursor');
                previewEl.classList.remove('prod-zoom-out-cursor');
            } else {
                previewEl.classList.add('prod-zoomed');
                previewEl.classList.remove('prod-normal');
                previewEl.style.backgroundSize = '220% auto';
                previewEl.classList.add('prod-zoom-out-cursor');
                previewEl.classList.remove('prod-zoom-in-cursor');
            }
        });

        // Set initial cursor style
        previewEl.classList.add('prod-zoom-in-cursor');

        // Ensure that zoom is off initially
        previewEl.classList.remove('prod-zoomed');
        previewEl.classList.add('prod-normal');
    };