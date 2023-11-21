### Командный проект. API для проекта YaMDb

### В чем идея проекта

```commandline
Проект YaMDb собирает отзывы пользователей на произведения. 
Сами произведения в YaMDb не хранятся, 
здесь нельзя посмотреть фильм или послушать музыку.
```
### Как установить: 

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/jisdtn/api_yamdb
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
### Примеры запросов к API.

```commandline
http://127.0.0.1:8000/api/v1/titles/{titles_id}/
```
```commandline
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
```commandline
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
