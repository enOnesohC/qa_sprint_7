import requests
import allure

from urls import URLS


class TestListOrders:
    @allure.title("Ручка /api/v1/orders")
    @allure.description("Получаем список заказов и смотрим количество заказов на странице")
    def test_get_list_orders_limit_10_positive(self):
        responce = requests.get(URLS.URL_MAIN + URLS.URL_TAKE_LIST_ORDERS + "?limit=10&page=0")

        assert responce.status_code == 200
        assert responce.json()["orders"] is not None

    @allure.title("Ручка /api/v1/orders")
    @allure.description("Получаем список заказов по id курьера")
    def test_get_list_orders_by_courier_id(self, login_new_courier):
        courier_id = login_new_courier
        responce = requests.get(URLS.URL_MAIN + URLS.URL_TAKE_LIST_ORDERS + "?courierId=" + str(courier_id))

        assert responce.status_code == 200
        assert responce.json() is not None

    @allure.title("Ручка /api/v1/orders")
    @allure.description("Получаем список заказов и выводим значение, больше максимально требуемого")
    def test_get_list_orders_limit_50_error(self):
        responce = requests.get(URLS.URL_MAIN + URLS.URL_TAKE_LIST_ORDERS + "?limit=50&page=0")
        assert responce.status_code == 409
        assert responce.json()["message"] == "Максимальное количество заказов на странице: 30"
