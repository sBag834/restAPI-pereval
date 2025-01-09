import os
import unittest
from database import Database


class TestDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.environ['FSTR_DB_HOST'] = 'localhost'
        os.environ['FSTR_DB_PORT'] = '5432'
        os.environ['FSTR_DB_LOGIN'] = 'postgres'
        os.environ['FSTR_DB_PASS'] = '36543654'

        cls.db_instance = Database()

    @classmethod
    def tearDownClass(cls):
        cls.db_instance.close()

    def test_submit_data(self):
        date_added = "2025-01-02T14:00:00"
        raw_data = '{"beautyTitle": "пер.", "title": "Тестовый перевал"}'
        images = '{"images": [{"id": 1, "title": "Тестовое изображение"}]}'

        new_id = self.db_instance.submit_data(date_added, raw_data, images)

        self.assertIsNotNone(new_id)

    def test_get_record_by_id(self):
        record = self.db_instance.get_record_by_id(16)  # Замените на ID, который вы знаете что он правильный
        self.assertIsNotNone(record)
        self.assertIsNotNone(record['raw_data'])

    def test_update_record(self):
        update_data = {
            "date_added": "2025-01-02T14:00:00",
            "raw_data": '{"beautyTitle": "пер.", "title": "Обновленный перевал"}',
            "images": '{"images": [{"id": 1, "title": "Обновленное изображение"}]}'
        }

        result = self.db_instance.update_record(15, update_data)  # Замените на ID, который вы знаете что он правильный
        self.assertTrue(result)

    def test_get_records_by_email(self):
        records = self.db_instance.get_records_by_email('meow@gmail.com')  # Замените на известный email
        self.assertIsInstance(records, list)


if __name__ == '__main__':
    unittest.main()