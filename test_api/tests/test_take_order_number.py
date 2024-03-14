import pytest
import allure
import requests
from urls import URLS
#import conftest

class TestTakeOrderNumber:
    @allure.title("Ручка /api/v1/orders/track")
    @allure.description("Создаём заказ, берём трек номер и получаем заказ по номеру")
    def test_take_order_number_positive(self, create_order):
        track = create_order
        responce = requests.get(URLS.URL_MAIN + URLS.URL_TAKE_ORDER_BY_NUMBER + "?t=" + str(track))
        assert responce.status_code == 200
        assert responce.json()["order"] is not None

    @allure.title("Ручка /api/v1/orders/track")
    @allure.description("Получаем заказ по неправильному номеру")
    def test_take_order_number_wrong_number_error(self):
        track = 999999
        responce = requests.get(URLS.URL_MAIN + URLS.URL_TAKE_ORDER_BY_NUMBER + "?t=" + str(track))
        assert responce.status_code == 404
        assert responce.json()["message"] == "Заказ не найден"

    @allure.title("Ручка /api/v1/orders/track")
    @allure.description("Получаем заказ без номера заказа")
    def test_take_order_number_without_number_error(self):
        responce = requests.get(URLS.URL_MAIN + URLS.URL_TAKE_ORDER_BY_NUMBER)
        assert responce.status_code == 400
        assert responce.json()["message"] == "Недостаточно данных для поиска"