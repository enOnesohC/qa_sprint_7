import string
import random
import requests
import allure
from urls import URLS


class Functions:
    @staticmethod
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # метод регистрации нового курьера возвращает список из логина и пароля
    # если регистрация не удалась, возвращает пустой список
    @staticmethod
    def register_new_courier_and_return_login_password():
        # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки

        # создаём список, чтобы метод мог его вернуть
        login_pass = []

        # генерируем логин, пароль и имя курьера
        login = Functions.generate_random_string(10)
        password = Functions.generate_random_string(10)
        first_name = Functions.generate_random_string(10)

        # собираем тело запроса
        payload = \
            {
                "login": login,
                "password": password,
                "firstName": first_name
            }

        # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
        response = requests.post(URLS.URL_MAIN + URLS.URL_CREATE_COURIER, data=payload)

        # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
        if response.status_code == 201:
            login_pass.append(login)
            login_pass.append(password)
            login_pass.append(first_name)

        # возвращаем список
        return login_pass

