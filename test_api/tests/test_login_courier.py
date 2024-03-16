import pytest
import requests
import functions
from urls import URLS
from data import LoginCourier
import allure


class TestLoginCourier:
    @allure.title("Ручка /api/v1/courier/login")
    @allure.description("Создаём нового курьера, затем логинимся и подтверждаем, что в теле ответа есть 'id' и там не пусто")
    def test_login_courier_positive(self):
        with allure.step('Получение данных зарегистрированного курьера'):
            login_pass = functions.Functions.register_new_courier_and_return_login_password()
            data = \
                {
                    "login": login_pass[0],
                    "password": login_pass[1]
                }
        with allure.step('Запрос на авторизацию'):
            response = requests.post(URLS.URL_MAIN + URLS.URL_LOGIN_COURIER, data)

        with allure.step('Проверки на статус и ответ'):
            assert "id" in response.json()
            assert response.json()["id"] != ""

    @allure.title("Ручка /api/v1/courier/login")
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

        with allure.step('Запрос на авторизацию с комбинацией заполненности логина и пароля'):
            response = requests.post(URLS.URL_MAIN + URLS.URL_LOGIN_COURIER, json=data)

        with allure.step('Проверки на статус и ответ'):
            assert response.status_code == 400
            assert response.json()["message"] == "Недостаточно данных для входа"

    @allure.title("Ручка /api/v1/courier/login")
    @allure.description("Логинимся с неправильным логином, ожидаем ошибку 404 и сообщение 'Учетная запись не найдена'")
    def test_login_courier_wrong_login(self):

        data = \
            {
                "login": "123141",
                "password": "qwerttyu"
            }
        with allure.step('Запрос на авторизацию с неправильным логином'):
            response = requests.post(URLS.URL_MAIN + URLS.URL_LOGIN_COURIER, data)

        with allure.step('Проверки на статус и ответ'):
            assert response.status_code == 404
            assert response.json()["message"] == "Учетная запись не найдена"
