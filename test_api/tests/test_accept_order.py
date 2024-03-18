import requests
from urls import URLS
import pytest
from data import AcceptOrder
import allure


class TestAcceptOrder:
    @allure.title("Ручка /api/v1/orders/accept/")
    @allure.description("Создаём заказ, получаем трек номер, создаём курьера, логинимся, получаем id, затем принимаем заказ")
    def test_accept_order_positive(self, login_new_courier, create_order):
        with allure.step('Получение трек-номера заказа'):
            track_number = create_order

        with allure.step('Создание нового курьера и получение его ID'):
            id_courier = login_new_courier

        with allure.step('Запрос на принятие заказа по трек-номеру и ID курьера'):
            response = requests.put(URLS.URL_MAIN + URLS.URL_ACCEPT_ORDER + str(track_number) + "?" + "courierId=" + str(id_courier))

        with allure.step('Проверки на статус и ответ'):
            assert response.status_code == 200
            assert response.json() == {'ok': True}

    @allure.title("Ручка /api/v1/orders/accept/")
    @allure.description(
        "Создаём курьера, логинимся, принимаем заказ с несуществующим id")
    def test_accept_order_wrong_track_number_error(self, login_new_courier):
        with allure.step('Создание нового курьера и получение его ID'):
            id_courier = login_new_courier

        with allure.step('Запрос на принятие заказа по неправильному трек-номеру и ID курьера'):
            response = requests.put(URLS.URL_MAIN + URLS.URL_ACCEPT_ORDER + "9999999" + "?" + "courierId=" + str(id_courier))

        with allure.step('Проверки на статус и ответ'):
            assert response.status_code == 404
            assert response.json()["message"] == "Заказа с таким id не существует"

    @allure.title("Ручка /api/v1/orders/accept/")
    @allure.description(
        "Создаём заказ, получаем трек номер, принимаем заказ с некорректным id курьера")
    def test_accept_order_wrong_courier_id_error(self, create_order):
        with allure.step('Получение трек-номера заказа'):
            track_number = create_order

        with allure.step('Запрос на принятие заказа по трек-номеру и некорректному ID курьера'):
            response = requests.put(URLS.URL_MAIN + URLS.URL_ACCEPT_ORDER + str(track_number) + "?" + "courierId=" + "999999")

        with allure.step('Проверки на статус и ответ'):
            assert response.status_code == 404
            assert response.json()["message"] == "Курьера с таким id не существует"

    @allure.title("Ручка /api/v1/orders/accept/")
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
        with allure.step('Запрос на принятие заказа по трек-номеру и некорректному ID курьера'):
            response = requests.put(URLS.URL_MAIN + URLS.URL_ACCEPT_ORDER + str(track_number) + "?" + "courierId=" + str(id_courier))

        with allure.step('Проверки на статус и ответ'):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для поиска"

    @allure.title("Ручка /api/v1/orders/accept/")
    @allure.description(
        "Создаём заказ, получаем трек номер, создаём двух курьеров, логинимся, получаем id, затем принимаем один заказ каждым курьером.")
    def test_accept_order_twice_error(self, create_order, login_new_courier):
        with allure.step('Получение трек-номера заказа'):
            track_number = create_order

        with allure.step('Создание двух новых курьеров и получение их ID'):
            id_courier_0 = login_new_courier
            id_courier_1 = login_new_courier

        with allure.step('Приём одного заказа двумя курьерами'):
            response = requests.put(URLS.URL_MAIN + URLS.URL_ACCEPT_ORDER + str(track_number) + "?" + "courierId=" + str(id_courier_0))
            response1 = requests.put(URLS.URL_MAIN + URLS.URL_ACCEPT_ORDER + str(track_number) + "?" + "courierId=" + str(id_courier_1))

        with allure.step('Проверки на статус и ответ'):
            assert response1.status_code == 409
            assert response1.json()["message"] == "Этот заказ уже в работе"
