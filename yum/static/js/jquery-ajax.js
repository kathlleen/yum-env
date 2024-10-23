$(document).ready(function () {
    $(document).on("click", ".add-to-cart", function (e) {

        // Блокируем его базовое действие
        e.preventDefault();
        // Берем элемент счетчика в значке корзины и берем оттуда значение
//        var goodsInCartCount = $("#cart-count");
//        var cartCount = parseInt(goodsInCartCount.text() || 0);

        // Получаем id товара из атрибута data-product-id
        var dish_id = $(this).data("dish-id");

        // Из атрибута href берем ссылку на контроллер django
        var add_to_cart_url = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу

        $.ajax({
            type: "POST",
            url: add_to_cart_url,
            data: {
                dish_id: dish_id,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {

                // Увеличиваем количество товаров в корзине (отрисовка в шаблоне)
//                cartCount++;
//                goodsInCartCount.text(cartCount);

                // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
                var cartItemsContainer = $("#cart-items-container");
                cartItemsContainer.html(data.cart_items_html);

            }
        });
    });
})



 // Ловим собыитие клика по кнопке удалить товар из корзины
$(document).on("click", ".remove-from-cart", function (e) {
    // Блокируем его базовое действие
    e.preventDefault();
    // Берем элемент счетчика в значке корзины и берем оттуда значение
    var goodsInCartCount = $("#cart-count");
    var cartCount = parseInt(goodsInCartCount.text() || 0);
    // Получаем id корзины из атрибута data-cart-id
    var cart_id = $(this).data("cart-id");
    // Из атрибута href берем ссылку на контроллер django
    var remove_from_cart = $(this).attr("href");
    // делаем post запрос через ajax не перезагружая страницу
    $.ajax({
        type: "POST",
        url: remove_from_cart,
        data: {
            cart_id: cart_id,
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        },
        success: function (data) {

            // Уменьшаем количество товаров в корзине (отрисовка)
            cartCount -= data.quantity_deleted;
            goodsInCartCount.text(cartCount);
            // Меняем содержимое корзины на ответ от django (новый отрисованный фрагмент разметки корзины)
            var cartItemsContainer = $("#cart-items-container");
            cartItemsContainer.html(data.cart_items_html);

        },
        error: function (data) {
            console.log("Ошибка при добавлении товара в корзину");
        },
    });
});


// Теперь + - количества товара
// Обработчик события для уменьшения значения
$(document).on("click", ".decrement", function () {
    // Берем ссылку на контроллер django из атрибута data-cart-change-url
    var url = $(this).data("cart-change-url");
    // Берем id корзины из атрибута data-cart-id
    var cartID = $(this).data("cart-id");
    // Ищем ближайшеий input с количеством
    var $input = $(this).closest('.input-group').find('.number');
    // Берем значение количества товара
    var currentValue = parseInt($input.val());
    // Если количества больше одного, то только тогда делаем -1
    if (currentValue > 1) {
        $input.val(currentValue - 1);
        // Запускаем функцию определенную ниже
        // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
        updateCart(cartID, currentValue - 1, -1, url);
    }
});
// Обработчик события для увеличения значения
$(document).on("click", ".increment", function () {
    // Берем ссылку на контроллер django из атрибута data-cart-change-url
    var url = $(this).data("cart-change-url");
    // Берем id корзины из атрибута data-cart-id
    var cartID = $(this).data("cart-id");
    // Ищем ближайшеий input с количеством
    var $input = $(this).closest('.input-group').find('.number');
    // Берем значение количества товара
    var currentValue = parseInt($input.val());
    $input.val(currentValue + 1);
    // Запускаем функцию определенную ниже
    // с аргументами (id карты, новое количество, количество уменьшилось или прибавилось, url)
    updateCart(cartID, currentValue + 1, 1, url);
});
function updateCart(cartID, quantity, change, url) {
    $.ajax({
        type: "POST",
        url: url,
        data: {
            cart_id: cartID,
            quantity: quantity,
            csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
        },
        success: function (data) {
            // Изменяем количество товаров в корзине
            var goodsInCartCount = $("#cart-count");
            var cartCount = parseInt(goodsInCartCount.text() || 0);
            cartCount += change;
            goodsInCartCount.text(cartCount);
            // Меняем содержимое корзины
            var cartItemsContainer = $("#cart-items-container");
            cartItemsContainer.html(data.cart_items_html);
        },
        error: function (data) {
            console.log("Ошибка при добавлении товара в корзину");
        },
    });
}


document.addEventListener("DOMContentLoaded", function() {
    const dropbtn = document.querySelector('.dropbtn');
    const dropdownContent = document.querySelector('.dropdown-content');

    // При клике на кнопку dropdown открываем/закрываем меню
    dropbtn.addEventListener('click', function(event) {
        event.preventDefault();
        dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
    });

    // Закрываем меню при клике вне dropdown
    document.addEventListener('click', function(event) {
        if (!dropbtn.contains(event.target) && !dropdownContent.contains(event.target)) {
            dropdownContent.style.display = 'none';
        }
    });
});

    document.addEventListener('DOMContentLoaded', function() {
        const cartBtn = document.getElementById('cart');
        const cartModal = document.getElementById('cartModal');
        const closeModal = document.getElementById('closeModal');
        const body = document.querySelector('body');

        // Открытие модального окна при клике на кнопку корзины
        cartBtn.addEventListener('click', function() {
            cartModal.style.display = 'block';
            body.style.overflow = body.style.overflow === 'hidden' ? 'auto' : 'hidden';
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
                body.style.overflow = 'auto';
            }
        });
    });



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

// profile

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