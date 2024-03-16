import pytest
import requests
import allure
from urls import URLS
from data import Order


class TestCreateOrder:

    @allure.title("Ручка /api/v1/orders")
    @allure.description("Создаём заказ c комбинациями цветов, ожидаем получить статус 201 и трек номер")
    @pytest.mark.parametrize(
        "body",
        [
            Order.body_0,
            Order.body_1,
            Order.body_2,
            Order.body_3
        ]
    )
    def test_take_order_positive(self, body):
        with allure.step('Запрос на создание заказа'):
            response = requests.post(URLS.URL_MAIN + URLS.URL_CREATE_ORDER, json=body)

        with allure.step('Проверки на статус и ответ'):
            assert response.status_code == 201
            assert response.json() is not None

    @allure.title("Ручка /api/v1/orders")
    @allure.description("Создаём заказ c корректными входными данными, ожидаем получить статус 201 и трек номер")
    def test_take_order_body_have_id(self):
        with allure.step('Запрос на создание заказа'):
            response = requests.post(URLS.URL_MAIN + URLS.URL_CREATE_ORDER, json=Order.body_0)

        with allure.step('Проверки на статус и ответ'):
            assert response.status_code == 201
            assert response.json()["track"] is not None
