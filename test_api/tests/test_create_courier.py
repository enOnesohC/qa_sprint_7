import pytest
import conftest
import requests
from urls import URLS
import string
import random
import allure
from data import Courier

class TestCreateCourier:

    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    @allure.title("Ручка /api/v1/courier")
    @allure.description("Создаём курьера, используя корректные данные")
    def test_create_courier_201(self):

        login = TestCreateCourier.generate_random_string(10)
        password = TestCreateCourier.generate_random_string(10)
        first_name = TestCreateCourier.generate_random_string(10)

        payload = \
            {
            "login": login,
            "password": password,
            "firstName": first_name
            }

        response = requests.post(URLS.URL_MAIN + URLS.URL_CREATE_COURIER, data=payload)

        assert response.status_code == 201
        assert response.json() == {'ok':True}

    @allure.description("Создаём курьера, затем создаём ещё одного курьера, с такими же данными. Должна быть неудача.")
    def test_create_simular_couriers_error_409(self):

        login_pass = conftest.register_new_courier_and_return_login_password()

        payload = \
            {
            "login": login_pass[0],
            "password": login_pass[1],
            "firstName": login_pass[2]
            }

        response = requests.post(URLS.URL_MAIN + URLS.URL_CREATE_COURIER, data=payload)

        assert response.status_code == 409
        assert response.json()["message"] == "Этот логин уже используется. Попробуйте другой."

    @allure.description("Пробуем создать курьера, комбинируя варианты заполнения обязательных полей")
    @pytest.mark.parametrize(
        "login, password, firstname",
        [
            Courier.COURIER_0,
            Courier.COURIER_1,
            Courier.COURIER_2,
            Courier.COURIER_3,
            Courier.COURIER_4,
            Courier.COURIER_5,
            Courier.COURIER_6
        ]
    )
    def test_create_courier_empty_field_error(self, login, password, firstname):

        payload = \
            {
                "login": login,
                "password": password,
                "firstName": firstname
            }
        response = requests.post(URLS.URL_MAIN + URLS.URL_CREATE_COURIER, data=payload)
        print(payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Недостаточно данных для создания учетной записи"