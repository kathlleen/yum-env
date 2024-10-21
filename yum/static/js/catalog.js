document.querySelector('.filter-btn').addEventListener('click', function() {
    var dropdownContent = document.querySelector('.dropdown-filters');
    dropdownContent.classList.toggle('show'); // Переключение класса "show"
});

document.addEventListener('click', function(event) {
    var dropdown = document.querySelector('.dropdown');
    if (!dropdown.contains(event.target)) {
        document.querySelector('.dropdown-content').classList.remove('show');
    }
});

document.addEventListener('DOMContentLoaded', function() {
        const cartBtn = document.getElementById('cart-btn');
        const cartModal = document.getElementById('cartModal');
        const body = document.querySelector('body');

        // Открытие модального окна при клике на кнопку корзины
        cartBtn.addEventListener('click', function() {
            cartModal.style.display = 'block';
            body.style.overflow = 'hidden';
        });

        // Закрытие модального окна при клике на кнопку закрытия
        closeModal.addEventListener('click', function() {
            cartModal.style.display = 'none';
            body.style.overflow = 'auto';
        });

        // Закрытие модального окна при клике вне области модального окна
        window.addEventListener('click', function(event) {
            if (event.target === cartModal) {
                cartModal.style.display = 'none';
            }
        });
    });