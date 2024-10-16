function openModal(dishId) {
    var modal = document.getElementById('modal-' + dishId);
    modal.style.display = "block";
}

// Функция для закрытия модального окна
function closeModal(dishId) {
    var modal = document.getElementById('modal-' + dishId);
    modal.style.display = "none";
}

// Закрытие модального окна, если пользователь нажал на затемненный фон
window.onclick = function(event) {
    var modals = document.getElementsByClassName('modal');
    for (var i = 0; i < modals.length; i++) {
        if (event.target == modals[i]) {
            modals[i].style.display = "none";
        }
    }
}