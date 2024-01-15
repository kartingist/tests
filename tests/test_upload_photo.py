from pprint import pprint

import pytest
import allure

from src.base_classes.response import validate_response

# @allure.feature('Создание нового пользователя')
# class TestCreateUser:
#     # # Конкретная пользовательская история или сценарий
#     # @allure.story('Пользовательская история') # Уровень важности теста
#     # @allure.severity(allure.severity_level.NORMAL) # Параметризация тестовых данных
#     # @pytest.mark.dependency(depends=["имя_функции_от_которой_зависит"],
#     #                         name="имя_текущей_функции")
#     # @pytest.mark.parametrize('test_data', []) # Добавьте ваши тестовые данные здесь
#     # Основная функция теста
#     def test_do_register(self, api_client):
#         # Динамический заголовок и описание для Allure
#         # allure.dynamic.title(f'Тест для {test_data}')
#         # allure.dynamic.description(f'Подробное описание теста для {test_data}')
#
#         # Шаг теста и его описание
#         with allure.step('Шаг 1: Отправка запроса и проверка статуса'):
#             json_data = {
#                 "email": "example@example.ru",
#                 "name": "Test_user",
#                 "password": "1234"
#             }
#
#             # Отправка запроса
#             response = api_client.do_register(json_data)
#             # Валидация ответа
#             json_response = validate_response(response, 200)
#             pprint(json_response)
#
#         # Шаг валидации ответа
#         with allure.step('Шаг 2: Валидация ответа'):
#             try:
#                 # Валидация ответа с помощью Pydantic модели
#                 DoRegisterErrorResponse(**json_response)
#             except ValidationError as e# @allure.feature('Создание нового пользователя')
# class TestCreateUser:
#     # # Конкретная пользовательская история или сценарий
#     # @allure.story('Пользовательская история') # Уровень важности теста
#     # @allure.severity(allure.severity_level.NORMAL) # Параметризация тестовых данных
#     # @pytest.mark.dependency(depends=["имя_функции_от_которой_зависит"],
#     #                         name="имя_текущей_функции")
#     # @pytest.mark.parametrize('test_data', []) # Добавьте ваши тестовые данные здесь
#     # Основная функция теста
#     def test_do_register(self, api_client):
#         # Динамический заголовок и описание для Allure
#         # allure.dynamic.title(f'Тест для {test_data}')
#         # allure.dynamic.description(f'Подробное описание теста для {test_data}')
#
#         # Шаг теста и его описание
#         with allure.step('Шаг 1: Отправка запроса и проверка статуса'):
#             json_data = {
#                 "email": "example@example.ru",
#                 "name": "Test_user",
#                 "password": "1234"
#             }
#
#             # Отправка запроса
#             response = api_client.do_register(json_data)
#             # Валидация ответа
#             json_response = validate_response(response, 200)
#             pprint(json_response)
#
#         # Шаг валидации ответа
#         with allure.step('Шаг 2: Валидация ответа'):
#             try:
#                 # Валидация ответа с помощью Pydantic модели
#                 DoRegisterErrorResponse(**json_response)
#             except ValidationError as e:
#                 # Прикрепление ответа к отчету в случае ошибки
#                 allure.attach(json.dumps(json_response, indent=2, ensure_ascii=False),
#                               name='Ответ API',
#                               attachment_type=allure.attachment_type.JSON)
#                 raise e
#
#         # Закрытие клиента
#         api_client.close()
#                 # Прикрепление ответа к отчету в случае ошибки
#                 allure.attach(json.dumps(json_response, indent=2, ensure_ascii=False),
#                               name='Ответ API',
#                               attachment_type=allure.attachment_type.JSON)
#                 raise e
#
#         # Закрытие клиента
#         api_client.close()
# json_response = validate_response(response, 200)
import requests
import pytest
from pydantic import ValidationError

from src.pydantic_schemas.create import CreateItemResponse, CreateItemErrorResponse
from src.pydantic_schemas.update import UpdateItemResponse
from src.pydantic_schemas.upload_photo import UploadPhotoItemErrorResponse


@allure.feature('Добавление фото товара')
class TestUploadPhoto:
    @allure.story('Позитивные сценарии добавления фото товара')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_upload_photo_positive(self, api_client):
        allure.dynamic.title(f'Заголовок теста')
        allure.dynamic.description(f'Подробное описание теста')
        # files = {
        #     'photo': open('../image.png', 'rb'),
        #     'id': (None, '1'),
        # }
        with open('../image.png', 'rb') as photo_file:
            files = {
                'photo': photo_file,
                'id': (None, 1),
            }

            with allure.step('Шаг 1: Отправка запроса и проверка статуса'):
                response = api_client.upload_photo(files=files)
                json_response = validate_response(response, 200)
                print(json_response)
            with allure.step('Шаг 2: Валидация ответа по схеме pydantic'):
                UpdateItemResponse(**json_response)

            with allure.step('Шаг 3: Проверка данных в ответе'):
                assert json_response.get('status') == 'ok', json_response
                assert json_response.get('method') == '/items/update', json_response
                assert json_response.get(
                    'result') == f'Фотография для товара {files.get("id")[1]} успешно загружена!', json_response

    @allure.story('Негативные сценарии добавления фото товара')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("file_path, item_id", [
        ('../image.png', None),  # Тест с фото, но без ID
        (None, 1),  # Тест с ID, но без фото
    ])
    def test_upload_photo_negative(self, api_client, file_path, item_id):
        allure.dynamic.title(f'Заголовок теста')
        allure.dynamic.description(f'Подробное описание теста')
        params = {
            'id': item_id
        }
        files = {}  # ID всегда передается, даже если он None
        if file_path:
            with open(file_path, 'rb') as photo_file:
                photo_data = photo_file.read()
                files['photo'] = ('filename.png', photo_data)

        with allure.step('Шаг 1: Отправка запроса и проверка статуса'):
            response = api_client.upload_photo(params=params, files=files)
            json_response = validate_response(response, 200)
        #
        with allure.step('Шаг 2: Валидация ответа по схеме pydantic'):
            UploadPhotoItemErrorResponse(**json_response)
        #
        with allure.step('Шаг 3: Проверка данных в ответе'):
            assert json_response.get('status') == 'error', json_response
        #
            if json_response.get('field_error') == 'id':
                assert json_response.get('error') == 'id_not_filled', json_response
                assert json_response.get('message') == 'Поле ID товара  не заполнено', json_response

            elif json_response.get('field_error') == 'photo':
                assert json_response.get('error') == 'photo_is_empty', json_response
                assert json_response.get('message') == 'Файл изображения не был загружен', json_response

            #
            else:
                assert False, json_response
