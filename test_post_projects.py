import pytest
import requests
import time

BASE_URL = "https://yougile.com"
API_KEY = " мой ключ "

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}


class TestPostProjects:
    
    def test_post_create_project_success(self):
        "Позитивный тест: создание проекта с валидными данными"
        
        unique_id = str(int(time.time() * 1000))[-6:]
        project_data = {
            "title": f"Тестовый проект {unique_id}",
            "idempotencyKey": f"key-{unique_id}"
        }
        
        response = requests.post(
            f'{BASE_URL}/api-v2/projects',
            json=project_data,
            headers=HEADERS
        )
        
        assert response.status_code == 201
        
        data = response.json()
        assert 'id' in data
    
    def test_post_create_project_without_title(self):
        "Негативный тест: создание проекта без поля title"
        
        unique_id = str(int(time.time() * 1000))[-6:]
        project_data = {
            "idempotencyKey": f"key-{unique_id}"
        }

        response = requests.post(
            f'{BASE_URL}/api-v2/projects',
            json=project_data,
            headers=HEADERS
        )
        
        assert response.status_code in [400, 422]

        