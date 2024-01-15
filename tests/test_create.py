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


@allure.feature('Создание товара')
class TestCreate:
    @allure.story('Позитивные сценарии создания товара')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("item_data", [
        {"name": "Шортики", "section": "Платья", "description": "Модное платье из новой коллекции!", "color": "RED",
         "size": 44, "price": 666, "params": "dress"},
        {"name": "Шортики", "section": "Платья", "description": "Модное платье из новой коллекции!"},

    ])
    def test_create_item_positive(self, api_client, item_data):
        allure.dynamic.title(f'Заголовок теста')
        allure.dynamic.description(f'Подробное описание теста')
        with allure.step('Шаг 1: Отправка запроса и проверка статуса'):
            response = api_client.create(json=item_data)
            json_response = validate_response(response, 200)
            pprint(json_response)
        with allure.step('Шаг 2: Валидация ответа по схеме pydantic'):
            CreateItemResponse(**json_response)

        with allure.step('Шаг 3: Проверка данных в ответе'):
            assert json_response.get('status') == 'ok', json_response
            assert json_response.get('method') == '/items/create', json_response
            result = json_response.get('result')
            assert result.get('color') == item_data.get('color')
            assert result.get('description') == item_data.get('description')
            assert result.get('name') == item_data.get('name')
            assert result.get('price') == item_data.get('price')
            assert result.get('section') == item_data.get('section')
            if item_data.get('params'):
                assert result.get('params') == item_data.get('params')

    @allure.story('Негативные сценарии создания товара')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("item_data", [
        {"name": "Шортики", "section": "Платья"},
        {"section": "Платья", "description": "Модное платье из новой коллекции!"},
        {"name": "Шортики", "description": "Модное платье из новой коллекции!"},
    ])
    def test_create_item_negative(self, api_client, item_data):
        allure.dynamic.title(f'Заголовок теста')
        allure.dynamic.description(f'Подробное описание теста')
        with allure.step('Шаг 1: Отправка запроса и проверка статуса'):
            response = api_client.create(json=item_data)
            json_response = validate_response(response, 200)

        with allure.step('Шаг 2: Валидация ответа по схеме pydantic'):
            CreateItemErrorResponse(**json_response)

        with allure.step('Шаг 3: Проверка данных в ответе'):
            assert json_response.get('status') == 'error', json_response

        if json_response.get('field_error') == 'description':
            assert json_response.get('error') == 'description_not_filled', json_response
            assert json_response.get('message') == 'Описание товара не заполнено!', json_response

        elif json_response.get('field_error') == 'name':
            assert json_response.get('error') == 'name_not_filled', json_response
            assert json_response.get('message') == 'Название товара не заполнено!', json_response

        elif json_response.get('field_error') == 'section':
            assert json_response.get('error') == 'section_not_found', json_response
            assert json_response.get('message') == 'Категория не найдена!', json_response

        else:
            assert False, json_response
