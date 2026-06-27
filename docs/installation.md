# Установка и запуск проекта

## Системные требования

- Python 3.12 или выше
- Git

## Клонирование репозитория

```bash
git clone https://github.com/coldisice/bookstore-management-system.git
cd bookstore-management-system
```

## Создание виртуального окружения

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Применение миграций

```bash
python manage.py migrate
```

## Создание администратора

```bash
python manage.py createsuperuser
```

## Запуск сервера разработки

```bash
python manage.py runserver
```

После запуска приложение будет доступно по адресу:

```
http://127.0.0.1:8000/
```

## Запуск автоматических тестов

```bash
python manage.py test
```

## Проверка качества кода

```bash
flake8 .
```