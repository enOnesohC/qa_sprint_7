import requests
from urls import URLS
import allure


class TestDeleteCourier:
    @allure.title("Ручка /api/v1/courier/")
    @allure.description("Создаём курьера, получаем id, делаем запрос на удаление")
    def test_delete_courier_positive(self, login_new_courier):
        courier_id = login_new_courier
        responce = requests.delete(URLS.URL_MAIN + URLS.URL_DELETE_COURIER + str(courier_id))

        assert responce.status_code == 200
        assert responce.json() == {'ok': True}

    @allure.title("Ручка /api/v1/courier/")
    @allure.description("Делаем запрос на удаление без указания id")
    def test_delete_courier_without_id_error(self):
        responce = requests.delete(URLS.URL_MAIN + URLS.URL_DELETE_COURIER)

        assert responce.status_code == 400
        assert responce.json() == "Недостаточно данных для удаления курьера"

    @allure.title("Ручка /api/v1/courier/")
    @allure.description("Делаем запрос на удаление, используя неправильный id")
    def test_delete_courier_id_not_exist_error(self):
        responce = requests.delete(URLS.URL_MAIN + URLS.URL_DELETE_COURIER + "999999")

        assert responce.status_code == 404
        assert responce.json()["message"] == "Курьера с таким id нет."
