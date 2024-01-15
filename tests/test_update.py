from pprint import pprint
import allure
from src.base_classes.response import validate_response
import pytest
from src.pydantic_schemas.update import UpdateItemResponse, UpdateItemErrorResponse


@allure.feature('Обновление товара')
class TestUpdate:
    @allure.story('Позитивные сценарии обновления товара')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("item_data", [
        {"id": 9, "name": "Платья", "section": "Платья", "description": "Модное платье из новой коллекции!",
         "color": "Черный", "size": "44, 46, 48", "price": 777, "params": "dress"},

        {"id": 1, "name": "Шортики", "section": "Платья", "description": "Модное платье из новой коллекции!"}
    ])
    def test_update_item_positive(self, api_client, item_data):
        allure.dynamic.title(f'Заголовок теста')
        allure.dynamic.description(f'Подробное описание теста')
        with allure.step('Шаг 1: Отправка запроса и проверка статуса'):
            response = api_client.update(json=item_data)
            json_response = validate_response(response, 200)
            pprint(json_response)
        with allure.step('Шаг 2: Валидация ответа по схеме pydantic'):
            UpdateItemResponse(**json_response)

        with allure.step('Шаг 3: Проверка данных в ответе'):
            assert json_response.get('status') == 'ok', json_response
            assert json_response.get('result') == 'Товар обновлен!', json_response
            assert json_response.get('method') == '/items/update', json_response

    @allure.story('Негативные сценарии обновления товара')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize("item_data", [
        {"name": "Шортики", "section": "Платья", "description": "Модное платье из новой коллекции!"},
        {"id": 1, "section": "Платья", "description": "Модное платье из новой коллекции!"},
        {"id": 1, "name": "Шортики", "description": "Модное платье из новой коллекции!"},
        {"id": 1, "name": "Шортики", "section": "Платья"},
        {"id": 1},

    ])
    def test_update_item_negative(self, api_client, item_data):
        allure.dynamic.title(f'Заголовок теста')
        allure.dynamic.description(f'Подробное описание теста')
        with allure.step('Шаг 1: Отправка запроса и проверка статуса'):
            response = api_client.update(json=item_data)
            json_response = validate_response(response, 200)

        with allure.step('Шаг 2: Валидация ответа по схеме pydantic'):
            try:
                UpdateItemErrorResponse(**json_response)
            except Exception as e:
                assert False, json_response

        with allure.step('Шаг 3: Проверка данных в ответе'):
            assert json_response.get('status') == 'error', json_response

            if json_response.get('field_error') == 'id':
                assert json_response.get('error') == 'id_not_filled', json_response
                assert json_response.get('message') == 'Поле ID товара  не заполнено', json_response

            elif json_response.get('field_error') == 'name':
                assert json_response.get('error') == 'name_not_filled', json_response
                assert json_response.get('message') == 'Название товара не заполнено!', json_response

            elif json_response.get('field_error') == 'section':
                assert json_response.get('error') == 'section_not_found', json_response
                assert json_response.get('message') == 'Категория не найдена!', json_response

            elif json_response.get('field_error') == 'description':
                assert json_response.get('error') == 'description_not_found', json_response
                assert json_response.get('message') == 'Описание товара не заполнено!', json_response

            else:
                assert False, json_response
