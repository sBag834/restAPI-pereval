import os
import psycopg2
from psycopg2.extras import RealDictCursor

class Database:
    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        """Подключение к базе данных."""
        host = os.getenv('FSTR_DB_HOST')
        port = os.getenv('FSTR_DB_PORT')
        login = os.getenv('FSTR_DB_LOGIN')
        password = os.getenv('FSTR_DB_PASS')
        dbname = 'pereval'

        try:
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=login,
                password=password,
                dbname=dbname
            )
            return conn
        except Exception as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise

    def submit_data(self, date_added, raw_data, images):
        """Добавление новой записи в таблицу перевалов."""
        status = 'new'
        with self.connection.cursor() as cursor:
            query = """
            INSERT INTO public.pereval_added (date_added, raw_data, images, status)
            VALUES (%s, %s::json, %s::json, %s)
            RETURNING id;
            """
            cursor.execute(query, (date_added, raw_data, images, status))
            self.connection.commit()
            return cursor.fetchone()[0]  # возвращаем ID новой записи

    def get_record_by_id(self, id):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM public.pereval_added WHERE id = %s;", (id,))
            return cursor.fetchone()

    

    def close(self):
        """Закрытие соединения с базой данных."""
        if self.connection:
            self.connection.close()