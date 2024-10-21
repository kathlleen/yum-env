// scripts.js

document.addEventListener('DOMContentLoaded', function() {
    const toggleButtons = document.querySelectorAll('.details-btn');

    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const orderDetails = this.closest('.order').querySelector('.order-details');
            orderDetails.style.display = orderDetails.style.display === 'none' || orderDetails.style.display === '' ? 'block' : 'none';
        });
    });
});


document.addEventListener("DOMContentLoaded", function() {
        const editButton = document.querySelector(".user-info .btn");
        const editForm = document.querySelector(".edit-form");

        editButton.addEventListener("click", function() {
            if (editForm.style.display === "none") {
                editForm.style.display = "block";
            } else {
                editForm.style.display = "none";
            }
        });
    });

document.addEventListener('DOMContentLoaded', function() {
        const cartBtn = document.getElementById('cart-btn');
        const cartModal = document.getElementById('cartModal');
        const closeModal = document.getElementById('closeModal');
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