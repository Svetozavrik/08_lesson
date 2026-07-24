import pytest
import requests
import time

BASE_URL = "https://yougile.com"
API_KEY = "мой ключ"

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}


class TestPutProject:
    
    @pytest.fixture
    def created_project_id(self):
        unique_id = str(int(time.time() * 1000))[-6:]
        project_data = {
            "title": f"Проект для PUT {unique_id}",
            "idempotencyKey": f"key-{unique_id}"
        }
        
        response = requests.post(
            f'{BASE_URL}/api-v2/projects',
            json=project_data,
            headers=HEADERS
        )
        
        if response.status_code == 201:
            return response.json()['id']
        else:
            pytest.skip("Не удалось создать проект для теста")
    
    def test_put_update_project_title_success(self, created_project_id):
        "Позитивный тест: обновление названия существующего проекта"
        
        new_title = f"Обновленный проект {str(int(time.time() * 1000))[-6:]}"
        
        response = requests.put(
            f'{BASE_URL}/api-v2/projects/{created_project_id}',
            json={"title": new_title},
            headers=HEADERS
        )
        
        assert response.status_code == 200
        get_response = requests.get(
            f'{BASE_URL}/api-v2/projects/{created_project_id}',
            headers=HEADERS
        )
        
        assert get_response.status_code == 200
        assert get_response.json()['title'] == new_title
    
    def test_put_update_nonexistent_project(self):
        "Негативный тест: обновление несуществующего проекта"
        
        fake_id = "00000000-0000-0000-0000-000000000000"
        
        response = requests.put(
            f'{BASE_URL}/api-v2/projects/{fake_id}',
            json={"title": "Новое название"},
            headers=HEADERS
        )
        
        assert response.status_code == 404


        