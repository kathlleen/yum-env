document.addEventListener('DOMContentLoaded', function() {
    function openModal(url) {
        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.text();
            })
            .then(html => {
                document.getElementById('modalContent').innerHTML = html;
                document.getElementById('universalModal').style.display = 'flex';
//                document.getElementById('universalModal').style.overflow-y = 'hidden';
                const closeButton = document.querySelector('.close-btn');

                if (closeButton) {
                    closeButton.addEventListener('click', function() {
                        document.getElementById('universalModal').style.display = 'none';
//                        document.getElementById('universalModal').style.overflow-y = 'auto';
                        document.getElementById('modalContent').innerHTML = ''; // Очищаем контент
                    });
                }
            })
            .catch(error => {
                console.error('There has been a problem with your fetch operation:', error);
            });
    }

    // Делегированный обработчик для всех событий внутри модального окна
    document.getElementById('modalContent').addEventListener('click', function (event) {
        const target = event.target;

        // События для корзины
        if (target.classList.contains('restaurant-toggle')) {
            handleCartToggle(target);
        }

    });

    function handleCartToggle(toggle) {
        const restaurantId = toggle.getAttribute('data-restaurant-id');
        const details = document.querySelector(`#restaurant-${restaurantId}`);

        // Закрываем все открытые разделы, кроме текущего
        document.querySelectorAll('.restaurant-details').forEach(detail => {
            if (detail !== details) {
                detail.classList.remove('open');
                const openToggle = detail.previousElementSibling;
                if (openToggle) openToggle.classList.remove('open');
            }
        });

        // Переключаем текущий раздел
        const isOpen = details.classList.contains('open');
        details.classList.toggle('open', !isOpen);
        toggle.classList.toggle('open', !isOpen);
    }


    // Пример: открытие модального окна для блюда
    document.querySelectorAll('.dish-card').forEach(card => {
        card.addEventListener('click', function(event) {
            const dishId = this.getAttribute('data-dish-id');
            const restaurantSlug = window.location.pathname.split('/')[2]; // Получаем slug ресторана из URL
            openModal(`/menu/${restaurantSlug}/dish-detail/${dishId}/`); // Формируем правильный URL
        });
    });

    // Пример: открытие модального окна для корзины
    document.getElementById('open-cart').addEventListener('click', function(event) {
        openModal(`/cart/`);
    });

    // Пример: открытие модального окна для акции
    document.querySelectorAll('.promotion-card').forEach(promo => {
        promo.addEventListener('click', function(event) {
            const promoId = this.getAttribute('data-promo-id');
            openModal(`/promotion-detail/${promoId}/`);
        });
    });
});
