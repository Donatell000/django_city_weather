## Стек технологий

- [⏳ celery](https://docs.celeryproject.org/en/stable/) | Распределённая очередь задач и фреймворк для асинхронной обработки задач
- [🐍 Django](https://www.djangoproject.com/) | Высокоуровневый веб-фреймворк для быстрой разработки на Python
- [🕰 django-celery-beat](https://github.com/celery/django-celery-beat) | Планировщик периодических задач для Celery и Django
- [🔒 django-cors-headers](https://pypi.org/project/django-cors-headers/) | Обработка CORS-заголовков для Django API
- [📡 djangorestframework](https://www.django-rest-framework.org/) | Мощный и гибкий инструментарий для создания REST API на Django
- [🔫 gunicorn](https://gunicorn.org/) | WSGI HTTP-сервер для UNIX-систем, совместимый с Django
- [🐘 psycopg2-binary](https://pypi.org/project/psycopg2-binary/) | Бинарный драйвер для подключения к PostgreSQL из Python
- [⚙️ python-dotenv](https://pypi.org/project/python-dotenv/) | Управление переменными окружения через `.env` файлы
- [📦 redis](https://pypi.org/project/redis/) | Redis-клиент для Python
- [🌐 requests](https://docs.python-requests.org/en/latest/) | Простая HTTP-библиотека для Python

---

## Быстрый старт

Для работы с проектом используются **Docker**.

#### 1. Клонирование репозитория и переход в папку проекта
```bash
git clone https://github.com/Donatell000/django_city_weather.git && cd django_city_weather
```

#### 2. Создание файлов окружения  
Создайте `.env` и `.env.db`, используя `.env.example`,\
`.env.db.example` и `.env.bot.example` в качестве шаблонов.

#### 3. Запуск контейнеров
```bash
make up
```

#### 4. Перезапуск контейнеров при необходимости
```bash
make down && make up
```

#### 5. (Опционально) Создание суперпользователя
```bash
make createsuperuser
```

---

## Получение API Token от OpenWeatherMap

- Перейдите на сайт: https://openweathermap.org/api
- Зарегистрируйтесь или войдите в существующий аккаунт
- Подтвердите адрес электронной почты
- Перейдите в раздел: https://home.openweathermap.org/api_keys
- Скопируйте сгенерированный ключ и добавьте его в .env файл как OPENWEATHER_API_KEY

---
## Архитектура

Проект представляет собой монолитное веб-приложение, реализованное на Django. Все компоненты развернуты в изолированных Docker-контейнерах:

#### Django Backend
- Веб-приложение на Django реализует как REST API, так и HTML/JS-интерфейс для взаимодействия с пользователем

- Получение прогноза погоды через запрос к внешнему API (OpenWeatherMap)

- При вводе города реализовано автодополнение с использованием JavaScript и API

- Сохраняется статистика по количеству запросов погоды каждого пользователя и общая статистика всех пользователей

- При повторном посещении пользователю предлагается посмотреть погоду в городе, который он ранее запрашивал

- Первично настроены Celery и Redis

#### Инфраструктура (Docker Compose)
Для развертывания проекта используется docker-compose, который автоматически поднимает все необходимые сервисы:

- PostgreSQL разворачивается из собственного Dockerfile \
Все переменные окружения вынесены в .env.db файл

- Redis используется как брокер сообщений для Celery

- Celery и Celery Beat запускаются как отдельные сервисы (celery_worker и celery_beat) с общим кодом Django-приложения

- Все сервисы объединены в единую пользовательскую сеть (django_network) с типом драйвера bridge

---

## Дополнительная информация

### Makefile
Проект использует `Makefile` для удобства работы. Примеры команд:
```bash
make up      # Запуск контейнеров
make down    # Остановка контейнеров
make logs    # Просмотр логов
make ps      # Просмотр запущенных контейнеров
```
