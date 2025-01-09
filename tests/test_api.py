import unittest
import requests

BASE_URL = 'http://localhost:5000/submitData'


class TestAPI(unittest.TestCase):

    def test_submit_data(self):
        data = {
            "date_added": "2025-01-02T14:00:00",
            "raw_data": '{"beautyTitle": "пер.", "title": "Тестовый перевал"}',
            "images": '{"images": [{"id": 1, "title": "Тестовое изображение"}]}'
        }
        response = requests.post(BASE_URL, json=data)

        self.assertEqual(response.status_code, 201)
        json_response = response.json()
        self.assertIn('id', json_response)

    def test_get_data(self):
        response = requests.get(f"{BASE_URL}/16")  # Замените на ID, который вы знаете что он правильный

        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIsNotNone(json_response['raw_data'])

    def test_patch_data(self):
        data = {
            "date_added": "2025-01-02T14:00:00",
            "raw_data": '{"beautyTitle": "пер.", "title": "Обновленный перевал"}',
            "images": '{"images": [{"id": 1, "title": "Обновленное изображение"}]}'
        }

        response = requests.patch(f"{BASE_URL}/15", json=data)  # Замените на ID, который вы знаете что он правильный

        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertEqual(json_response['state'], 1)

    def test_get_records_by_email(self):
        response = requests.get(f"{BASE_URL}/?user__email=meow@gmail.com")  # Замените на известный email

        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIsInstance(json_response, list)


if __name__ == '__main__':
    unittest.main()
