import uuid

import psycopg2

from src.config import DB_NAME, DB_USER, DB_PASS, DB_HOST, DB_PORT

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    port=DB_PORT
)
cursor = conn.cursor()

user_id = uuid.uuid4()
user_pass = get_password_hash("123")
admin_id = uuid.uuid4()
admin_pass = get_password_hash("123")

# Выполнение SQL запроса для добавления данных в таблицу
insert_query = f"""
INSERT INTO project (title, parent_id)
VALUES ('Создать приложение менеджера проектов', null), 
       ('Создать БД', 1),
       ('Реализовать логику', 1),
       ('Попить пива', null),
       ('Получить ЗП', null);
       
INSERT INTO "user" (user_id, email, is_active, hashed_password, roles)
VALUES (UUID('{user_id}'), 'user@example.com', True, '{user_pass}', 'user'),
       (UUID('{admin_id}'), 'admin@example.com', True, '{admin_pass}', 'admin');
       
INSERT INTO task (title, status, type, project_id, user_id)
VALUES ('БД пользователей', 'done', 'technical_specialist', 2, UUID('{user_id}')),
       ('БД задач', 'progress', 'technical_specialist', 2, UUID('{admin_id}')),
       ('БД проектов', 'done', 'technical_specialist', 2, UUID('{user_id}')),
       ('Запись пользователей', 'new', 'technical_specialist', 3, UUID('{user_id}')),
       ('CRUD задач', 'new', 'technical_specialist', 3, UUID('{admin_id}')),
       ('CRUD проектов', 'progress', 'technical_specialist', 3, UUID('{user_id}')),
       ('Попить пива', 'progress', 'manager', 4, UUID('{admin_id}')),
       ('ЗП получить все', 'new', 'manager', 5, UUID('{user_id}')),
       ('ЗП получить', 'new', 'manager', 5, UUID('{admin_id}'));
"""
cursor.execute(insert_query)

# Фиксация изменений и закрытие подключения
conn.commit()
cursor.close()
conn.close()