import conftest
import requests
from urls import URLS
import pytest
from data import AcceptOrder
import allure


class TestAcceptOrder:
    @allure.title("Ручка /api/v1/orders/accept/")
    @allure.description("Создаём заказ, получаем трек номер, создаём курьера, логинимся, получаем id, затем принимаем заказ")
    def test_accept_order_positive(self):
        track_number = conftest.create_order()
        id_courier = conftest.login_new_courier()
        response = requests.put(URLS.URL_MAIN + URLS.URL_ACCEPT_ORDER + str(track_number) + "?" + "courierId=" + str(id_courier))

        assert response.status_code == 200
        assert response.json() == {'ok': True}

    @allure.description(
        "Создаём курьера, логинимся, принимаем заказ с несуществующим id")
    def test_accept_order_wrong_track_number_error(self):
        id_courier = conftest.login_new_courier()
        response = requests.put(URLS.URL_MAIN + URLS.URL_ACCEPT_ORDER + "9999999" + "?" + "courierId=" + str(id_courier))

        assert response.status_code == 404
        assert response.json()["message"] == "Заказа с таким id не существует"

    @allure.description(
        "Создаём заказ, получаем трек номер, принимаем заказ с некорректным id курьера")
    def test_accept_order_wrong_courier_id_error(self):
        track_number = conftest.create_order()
        response = requests.put(URLS.URL_MAIN + URLS.URL_ACCEPT_ORDER + str(track_number) + "?" + "courierId=" + "999999")

        assert response.status_code == 404
        assert response.json()["message"] == "Курьера с таким id не существует"

    @allure.description(
        "Принимаем заказ с комбинациями заполненности полей: трек номер и курьер")
    @pytest.mark.parametrize(
        "track_number, id_courier",
        [
            AcceptOrder.Accept_0,
            AcceptOrder.Accept_1,
            AcceptOrder.Accept_2
        ]
    )
    def test_accept_order_without_courier_id_or_track_number_error(self, track_number, id_courier):
        response = requests.put(URLS.URL_MAIN + URLS.URL_ACCEPT_ORDER + str(track_number) + "?" + "courierId=" + str(id_courier))

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для поиска"

    @allure.description(
        "Создаём заказ, получаем трек номер, создаём двух курьеров, логинимся, получаем id, затем принимаем один заказ каждым курьером.")
    def test_accept_order_twice_error(self):
        track_number = conftest.create_order()
        id_courier_0 = conftest.login_new_courier()
        id_courier_1 = conftest.login_new_courier()
        response = requests.put(URLS.URL_MAIN + URLS.URL_ACCEPT_ORDER + str(track_number) + "?" + "courierId=" + str(id_courier_0))
        response1 = requests.put(URLS.URL_MAIN + URLS.URL_ACCEPT_ORDER + str(track_number) + "?" + "courierId=" + str(id_courier_1))

        assert response1.status_code == 409
        assert response1.json()["message"] == "Этот заказ уже в работе"
