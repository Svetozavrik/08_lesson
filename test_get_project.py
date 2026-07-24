import pytest
import requests
import time

BASE_URL = "https://yougile.com"
API_KEY = "мой ключ"

HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}


class TestGetProject:
    
    def test_get_project_by_id_success(self):
        "Позитивный тест: получаем список проектов"
        
        unique_id = str(int(time.time() * 1000))[-6:]
        project_data = {
            "title": f"Проект для GET {unique_id}",
            "idempotencyKey": f"key-{unique_id}"
        }
        
        create_response = requests.post(
            f'{BASE_URL}/api-v2/projects',
            json=project_data,
            headers=HEADERS
        )
        
        assert create_response.status_code == 201
        project_id = create_response.json()['id']
        
        get_response = requests.get(
            f'{BASE_URL}/api-v2/projects/{project_id}',
            headers=HEADERS
        )
       
        assert get_response.status_code == 200
        data = get_response.json()
        assert data['id'] == project_id
        assert data['title'] == project_data['title']
    
    def test_get_nonexistent_project(self):
        "Негативный тест: получаем несуществующий проект"
        
        fake_id = "00000000-0000-0000-0000-000000000000"
        
        response = requests.get(
            f'{BASE_URL}/api-v2/projects/{fake_id}',
            headers=HEADERS
        )
        
        assert response.status_code == 404

