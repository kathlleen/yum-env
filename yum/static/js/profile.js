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

document.addEventListener("DOMContentLoaded", function () {
    const avatars = document.querySelectorAll('.avatars button');
    const hiddenInput = document.getElementById('selected_avatar');

    avatars.forEach(button => {
        button.addEventListener("click", function (event) {
            event.preventDefault();

            // Удаляем класс 'active_avatar' у всех кнопок
            avatars.forEach(btn => btn.classList.remove('active_avatar'));

            // Добавляем класс 'active_avatar' к нажатой кнопке
            this.classList.add('active_avatar');
            const selectedAvatar = this.getAttribute('data-avatar');

            hiddenInput.value = selectedAvatar;
        });
    });
});
