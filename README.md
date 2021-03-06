# API для системы опросов пользователей
Задача: спроектировать и разработать API для системы опросов пользователей
Тестовое задание для компании "Фабрика Решений"
> После локального запуска проекта можете посмотреть автодокументацию на swagger(drf-yasg) доступно по адресу http://localhost:8000/swagger/

## Описание ТЗ:
### Функционал для администратора системы:

- авторизация в системе (регистрация не нужна)
- добавление/изменение/удаление опросов. Атрибуты опроса: название, дата старта, дата окончания, описание. После создания поле "дата старта" у опроса менять нельзя
- добавление/изменение/удаление вопросов в опросе. Атрибуты вопросов: текст вопроса, тип вопроса (ответ текстом, ответ с выбором одного варианта, ответ с выбором нескольких вариантов)

### Функционал для пользователей системы:

- получение списка активных опросов
- прохождение опроса: опросы можно проходить анонимно, в качестве идентификатора пользователя в API передаётся числовой ID, по которому сохраняются ответы пользователя на вопросы; один пользователь может участвовать в любом количестве опросов
- получение пройденных пользователем опросов с детализацией по ответам (что выбрано) по ID уникальному пользователя

## Установка
Установка происходит локально
* Скопируйте репозиторий:
```
git clone https://github.com/Iki-oops/FR_test.git
```
* Установите виртуальное окружение и активируйте:
```
python -m venv venv
source venv/Scripts/activate
```
* Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
* Выполните следующие команды:
```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```
Команда manage.py createsuperuser создает суперпользователя, после выполнения этой команды появятся бланки для заполнения. Заполните их.
* Команда для запуска приложения
```
python manage.py runserver
```
* Приложение будет доступно по адресу: http://localhost:8000/

## Пользовательские роли
### Аноним может:
* Получить все списки опросов (http://localhost:8000/api/v1/polls)
* Получить все вопросы определенного опроса (http://localhost:8000/api/v1/polls/{poll_id}/questions/)
* Отвечать в любом количестве на вопросы анонимно (http://localhost:8000/api/v1/polls/{poll_id}/questions/{question_id}/answer/)
* Получить все вопросы, на которые ответил пользователь (http://localhost:8000/api/v1/answers/)
> Но для этого сначала нужно получить cookie http://localhost:8000/api/v1/start-polling/, удалить по http://localhost:8000/api/v1/delete-test-cookie/
### Администратор может:
* Все тоже что и аноним
* Авторизироваться в системе. Атрибуты: username, password (http://localhost:8000/api/v1/get-token/)
* Добавить/изменить/удалить опросы. Атрибуты опроса: name, start_date, end_date, description, questions. После создания поле "дата старта" у опроса менять нельзя (http://localhost:8000/api/v1/poll/)
* Добавить/изменить/удалить вопросы в опросе. Атрибуты вопросов: text, type (http://localhost:8000/api/v1/polls/{poll_id}/questions/)

## Стек технологий
Python 3, Django 2.2.10, Django REST Framework, SQLite, Simple-JWT
