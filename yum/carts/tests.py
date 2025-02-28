from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from menu.models import Dish, Categories
from restaurans.models import Restaurans
from carts.models import Cart
from decimal import Decimal

class CartAjaxTestCase(TestCase):

    def setUp(self):
        """Создаем тестовые данные"""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")

        self.category = Categories.objects.create(name="Закуски", slug="snacks")
        self.restaurant = Restaurans.objects.create(name="Тестовый ресторан", slug="test-restaurant")

        self.dish = Dish.objects.create(
            name="Пицца",
            slug="pizza",
            price=Decimal("10.00"),
            category=self.category,
            restaurant=self.restaurant
        )

        self.cart_url = reverse("carts:cart_add")

        session = self.client.session
        session.create()
        session.save()

    def test_add_to_cart_ajax(self):
        """Проверяем, что товар добавляется в корзину через AJAX без обновления страницы"""

        self.client.login(username="testuser", password="testpassword")

        response = self.client.post(self.cart_url, {
            "dish_id": self.dish.id,
            "rest_id": self.restaurant.id,
            "quantity": 1
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest', enforce_csrf_checks=False)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cart.objects.count(), 1)

        cart_item = Cart.objects.first()
        self.assertEqual(cart_item.user, self.user)
        self.assertEqual(cart_item.dish, self.dish)
        self.assertEqual(cart_item.quantity, 1)

        self.assertEqual(response["Content-Type"], "application/json")
        self.assertIn("success", response.json())
        self.assertTrue(response.json()["success"])





class CartQuantityChangeAjaxTestCase(TestCase):

    def setUp(self):
        """Создаем тестовые данные"""
        self.user = get_user_model().objects.create_user(username="testuser", password="testpassword")

        self.category = Categories.objects.create(name="Закуски", slug="snacks")
        self.restaurant = Restaurans.objects.create(name="Тестовый ресторан", slug="test-restaurant")

        self.dish = Dish.objects.create(
            name="Пицца",
            slug="pizza",
            price=Decimal("10.00"),
            category=self.category,
            restaurant=self.restaurant
        )

        # Создаем корзину с 1 товаром
        self.cart = Cart.objects.create(
            user=self.user,
            dish=self.dish,
            quantity=1
        )

        # URL для обработки изменения корзины
        self.cart_change_url = reverse("carts:cart_change")

        session = self.client.session
        session.create()
        session.save()

    def test_increment_cart_quantity_ajax(self):
        """Проверяем увеличение количества товара в корзине через AJAX"""

        self.client.login(username="testuser", password="testpassword")

        # Ищем текущую корзину на странице
        initial_quantity = self.cart.quantity

        # Делаем запрос на увеличение количества товара через AJAX
        response = self.client.post(self.cart_change_url, {
            "cart_id": self.cart.id,
            "quantity": initial_quantity + 1,
            "rest_id": self.restaurant.id
        }, HTTP_X_REQUESTED_WITH='XMLHttpRequest', enforce_csrf_checks=False)

        # Проверяем, что ответ успешный
        self.assertEqual(response.status_code, 200)

        # Проверяем, что количество товара в корзине обновилось
        self.cart.refresh_from_db()
        self.assertEqual(self.cart.quantity, initial_quantity + 1)

        # Проверяем, что в ответе содержится HTML для обновленной корзины
        self.assertIn("cart-items-container", response.json()["cart_items_html"])
        self.assertIn("Пицца", response.json()["cart_items_html"])

    def test_decrement_cart_quantity_ajax(self):
        """Проверяем уменьшение количества товара в корзине через AJAX"""

        self.client.login(username="testuser", password="testpassword")

        # Ищем текущую корзину на странице
        initial_quantity = self.cart.quantity

        # Уменьшаем количество товара только если оно больше 1
        if initial_quantity > 1:
            response = self.client.post(self.cart_change_url, {
                "cart_id": self.cart.id,
                "quantity": initial_quantity - 1,
                "rest_id": self.restaurant.id
            }, HTTP_X_REQUESTED_WITH='XMLHttpRequest', enforce_csrf_checks=False)

            # Проверяем, что ответ успешный
            self.assertEqual(response.status_code, 200)

            # Проверяем, что количество товара в корзине уменьшилось
            self.cart.refresh_from_db()
            self.assertEqual(self.cart.quantity, initial_quantity - 1)

            # Проверяем, что в ответе содержится HTML для обновленной корзины
            self.assertIn("cart-items-container", response.json()["cart_items_html"])
            self.assertIn("Пицца", response.json()["cart_items_html"])


