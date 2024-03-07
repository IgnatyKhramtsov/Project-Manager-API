## Клонируйте проект
``` git clone https://github.com/IgnatyKhramtsov/Project-Manager-API.git ```

## Установите зависимости проекта
``` pip install -r requirements.txt ```

## Задайте параметры базы данный в файле **.env** по шаблону внутри.

## Задать папку **src** как **Sources root**

## Запустите миграцию базы данных
``` alembic upgrade head ```

## Запустите скрипт для первичной инициализации базы данных ее тестовыми данными, из корневой папки проекта:
``` python script_db.py```


## Запустите проект, либо из консоли, перейдя в папку **src**, либо из файла **main**:
``` uvicorn main:app --reload ```

## Для запуска через Docker:
### - заполните файл **.env_non_dev** по шаблону
### - для запуска введите ``` docker-compose up --build ```

## Перейти по адресу: http://localhost:8001/

## Пользователи:

USER: username: user@example.com
      password: 123

ADMIN: username: admin@example.com
       password: 123