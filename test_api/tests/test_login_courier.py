import pytest
import requests
import conftest
from urls import URLS
from data import LoginCourier
import allure


class TestLoginCourier:
    @allure.title("Ручка /api/v1/courier/login")
    @allure.description("Создаём нового курьера, затем логинимся и подтверждаем, что в теле ответа есть 'id' и там не пусто")
    def atest_login_courier_positive(self):
        login_pass = conftest.register_new_courier_and_return_login_password()
        data = \
            {
                "login": login_pass[0],
                "password": login_pass[1]
            }
        response = requests.post(URLS.URL_MAIN + URLS.URL_LOGIN_COURIER, data)
        assert "id" in response.json()
        assert response.json()["id"] != ""

    @allure.description("Пробуем залогиниться, используя некорректные данные, ожидаем получить ошибку 400 и текст 'Недостаточно данных для входа'")
    @pytest.mark.parametrize(
        "login, password",
        [
            LoginCourier.Login_0,
            LoginCourier.Login_1,
            LoginCourier.Login_2
        ]
    )
    def test_login_courier_empty_fields_error(self, login, password):
        data = \
            {
                "login": login,
                "password": password
            }
        response = requests.post(URLS.URL_MAIN + URLS.URL_LOGIN_COURIER, json=data)

        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.description("Создаём нового курьера, затем логинимся с неправильным логином, ожадаем ошибку 404 и сообщение 'Учетная запись не найдена'")
    def atest_login_courier_wrong_login(self):

        login_pass = conftest.register_new_courier_and_return_login_password()
        data = \
            {
                "login": "123141",
                "password": login_pass[1]
            }
        response = requests.post(URLS.URL_MAIN + URLS.URL_LOGIN_COURIER, data)
        assert response.status_code == 404
        assert response.json()["message"] == "Учетная запись не найдена"
