import requests
import random
import string

from data import Order
from urls import URLS


# метод регистрации нового курьера возвращает список из логина и пароля
# если регистрация не удалась, возвращает пустой список
def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
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


def login_new_courier():
    login_pass = register_new_courier_and_return_login_password()

    data =\
        {
            "login": login_pass[0],
            "password": login_pass[1]
        }
    response = requests.post(URLS.URL_MAIN + URLS.URL_LOGIN_COURIER, data)

    return response.json()["id"]


def create_order():
    response = requests.post(URLS.URL_MAIN + URLS.URL_CREATE_ORDER, json = Order.body_0)
    return response.json()["track"]


