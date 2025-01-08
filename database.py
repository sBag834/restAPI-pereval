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

    def update_record(self, id, data):
        with self.connection.cursor() as cursor:
            # Получаем текущую запись для проверки статуса
            cursor.execute("SELECT status FROM public.pereval_added WHERE id = %s;", (id,))
            record_status = cursor.fetchone()

            if record_status and record_status[0] == 'new':
                # Обновляем только разрешенные поля
                updates = []
                values = []

                if 'date_added' in data:
                    updates.append("date_added = %s")
                    values.append(data['date_added'])

                if 'raw_data' in data:
                    updates.append("raw_data = %s::json")
                    values.append(data['raw_data'])

                if 'images' in data:
                    updates.append("images = %s::json")
                    values.append(data['images'])

                if updates:
                    query = f"UPDATE public.pereval_added SET {', '.join(updates)} WHERE id = %s;"
                    values.append(id)
                    cursor.execute(query, tuple(values))
                    self.connection.commit()
                    return True

            return False

    def get_records_by_email(self, email):
        with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM public.pereval_added WHERE raw_data->>'user'->>'email' = %s;", (email,))
            return cursor.fetchall()

    def close(self):
        """Закрытие соединения с базой данных."""
        if self.connection:
            self.connection.close()