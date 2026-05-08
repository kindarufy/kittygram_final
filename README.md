# Kittygram Final

**Kittygram Final** - учебный проект Яндекс Практикума по контейнеризации и CI/CD.

Проект представляет собой социальную сеть для публикации карточек котиков. Пользователь может зарегистрироваться, войти в аккаунт, добавить котика с фотографией, цветом, годом рождения и достижениями, а также просматривать карточки других пользователей.

Основной акцент проекта - не только на Django/React-приложении, но и на полноценной инфраструктуре: запуске приложения в Docker-контейнерах, настройке PostgreSQL, Nginx gateway, Docker volumes и автоматическом деплое через GitHub Actions.

---

## Что реализовано

- Контейнеризация backend-приложения на Django.
- Контейнеризация frontend-приложения на React.
- Отдельный контейнер gateway на Nginx.
- Подключение PostgreSQL в отдельном контейнере.
- Использование Docker volumes для хранения:
  - данных PostgreSQL;
  - собранной статики backend и frontend;
  - пользовательских media-файлов.
- Разделение локального и production-запуска через разные compose-файлы.
- Настройка переменных окружения через `.env` и `.env.example`.
- Настройка CI/CD через GitHub Actions:
  - проверка backend-кода на соответствие PEP8;
  - запуск тестов backend;
  - запуск тестов frontend;
  - сборка Docker-образов;
  - публикация образов на Docker Hub;
  - автоматический деплой на удалённый сервер по SSH;
  - применение миграций;
  - сборка статики;
  - Telegram-уведомление об успешном деплое.

---

## Технологии

### Backend

- Python 3.12
- Django 5.1.1
- Django REST Framework
- Djoser
- Token Authentication
- PostgreSQL
- Pillow
- Gunicorn

### Frontend

- JavaScript
- React 17
- React Router
- CSS Modules

### Infrastructure / DevOps

- Docker
- Docker Compose
- Nginx
- PostgreSQL 13
- Docker Hub
- GitHub Actions
- SSH deploy
- Telegram notifications

---

## Архитектура проекта

Приложение запускается в нескольких контейнерах:

| Контейнер | Назначение |
|---|---|
| `backend` | Django API, админка, работа с пользователями, котиками и достижениями |
| `frontend` | React-приложение, сборка SPA-статики |
| `gateway` | Nginx, маршрутизация запросов и раздача статики/media |
| `db` | PostgreSQL, хранение данных приложения |

Схема обработки запросов:

```text
Пользователь → Nginx gateway → backend / frontend static / media
                         ↓
                    PostgreSQL
```

Nginx обрабатывает входящие запросы:

- `/api/` — проксирует в backend;
- `/admin/` — проксирует в backend;
- `/media/` — раздаёт загруженные изображения;
- остальные запросы — отдаёт frontend SPA.

---

## Структура проекта

```text
kittygram_final/
├── .github/workflows/main.yml       # CI/CD workflow
├── backend/                         # Django backend
│   ├── cats/                        # Приложение с моделями котиков и достижений
│   ├── kittygram_backend/           # Настройки Django-проекта
│   ├── Dockerfile                   # Dockerfile backend-образа
│   ├── manage.py
│   └── requirements.txt
├── frontend/                        # React frontend
│   ├── Dockerfile                   # Dockerfile frontend-образа
│   ├── public/
│   └── src/
├── nginx/                           # Nginx gateway
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml               # Локальный запуск контейнеров
├── docker-compose.production.yml    # Production-запуск на сервере
├── kittygram_workflow.yml           # Копия workflow для проверки ревьюером
├── tests.yml                        # Данные для автопроверки
├── .env.example                     # Пример переменных окружения
└── README.md
```

---

## Переменные окружения

Перед запуском создайте файл `.env` в корне проекта по примеру `.env.example`:

```env
POSTGRES_DB=kittygram
POSTGRES_USER=kittygram_user
POSTGRES_PASSWORD=kittygram_password
DB_HOST=db
DB_PORT=5432
SECRET_KEY=change-me
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,backend,testserver
CSRF_TRUSTED_ORIGINS=http://localhost:9000,http://127.0.0.1:9000
STATIC_ROOT=/backend_static/static
```

Для production-окружения значения нужно заменить на реальные:

- сложный `SECRET_KEY`;
- домен проекта в `ALLOWED_HOSTS`;
- домен проекта в `CSRF_TRUSTED_ORIGINS`;
- надёжный пароль PostgreSQL.

Файл `.env` не должен попадать в репозиторий.

---

## Локальный запуск через Docker Compose

Клонируйте репозиторий:

```bash
git clone https://github.com/kindarufy/kittygram_final.git
cd kittygram_final
```

Создайте `.env`:

```bash
cp .env.example .env
```

Соберите и запустите контейнеры:

```bash
docker compose up --build
```

В отдельном терминале выполните миграции:

```bash
docker compose exec backend python manage.py migrate
```

Соберите статику backend:

```bash
docker compose exec backend python manage.py collectstatic --no-input
```

После запуска приложение будет доступно по адресу:

```text
http://localhost:9000/
```

Админка Django:

```text
http://localhost:9000/admin/
```

API:

```text
http://localhost:9000/api/
```

---

## Production-запуск

Для production используется файл `docker-compose.production.yml`.

Он запускает контейнеры из готовых Docker Hub образов:

- `kindarufy/kittygram_backend:latest`
- `kindarufy/kittygram_frontend:latest`
- `kindarufy/kittygram_gateway:latest`
- `postgres:13`

Запуск на сервере:

```bash
sudo docker compose -f docker-compose.production.yml pull
sudo docker compose -f docker-compose.production.yml up -d
```

После запуска нужно применить миграции и собрать статику:

```bash
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic --no-input
```

В проекте эти команды автоматизированы через GitHub Actions.

---

## CI/CD

Workflow находится в файле:

```text
.github/workflows/main.yml
```

При push в ветку `main` GitHub Actions выполняет следующие этапы:

1. Проверяет backend:
   - устанавливает Python;
   - поднимает PostgreSQL service-контейнер;
   - устанавливает зависимости;
   - запускает `flake8`;
   - запускает Django tests.

2. Проверяет frontend:
   - устанавливает Node.js;
   - устанавливает зависимости через `npm ci`;
   - запускает frontend tests.

3. Собирает и публикует Docker-образы:
   - backend;
   - frontend;
   - gateway.

4. Подключается к серверу по SSH:
   - копирует `docker-compose.production.yml`;
   - скачивает свежие образы;
   - перезапускает контейнеры;
   - применяет миграции;
   - собирает статику.

5. Отправляет Telegram-уведомление об успешном деплое.

Для работы workflow в GitHub Secrets должны быть добавлены переменные:

| Secret | Назначение |
|---|---|
| `DOCKER_USERNAME` | логин Docker Hub |
| `DOCKER_PASSWORD` | пароль или access token Docker Hub |
| `HOST` | IP-адрес или домен сервера |
| `USER` | пользователь на сервере |
| `SSH_KEY` | приватный SSH-ключ для доступа к серверу |
| `TELEGRAM_TO` | ID пользователя или чата Telegram |
| `TELEGRAM_TOKEN` | токен Telegram-бота |

---

## API

Основные эндпоинты:

| Метод | Endpoint | Описание |
|---|---|---|
| `GET` | `/api/cats/` | Получить список котиков |
| `POST` | `/api/cats/` | Добавить котика |
| `GET` | `/api/cats/{id}/` | Получить карточку котика |
| `PUT/PATCH` | `/api/cats/{id}/` | Изменить карточку котика |
| `DELETE` | `/api/cats/{id}/` | Удалить карточку котика |
| `GET` | `/api/achievements/` | Получить список достижений |
| `POST` | `/api/users/` | Зарегистрировать пользователя |
| `POST` | `/api/token/login/` | Получить токен авторизации |
| `POST` | `/api/token/logout/` | Удалить токен авторизации |

---

## Тестирование

### Backend

```bash
cd backend
python manage.py test
```

Проверка стиля кода:

```bash
python -m flake8 backend/
```

### Frontend

```bash
cd frontend
npm test -- --watchAll=false --passWithNoTests
```

### Автотесты Практикума

В корне проекта есть файл `tests.yml` с данными для проверки:

```yaml
repo_owner: kindarufy
kittygram_domain: https://kittygram-nikol.duckdns.org
taski_domain: https://taski-nikol.duckdns.org
dockerhub_username: kindarufy
```

---

## Что было сделано в рамках проекта

В рамках финального задания были выполнены следующие задачи:

- написан Dockerfile для backend-приложения;
- настроен запуск Django через Gunicorn;
- настроена работа Django с PostgreSQL;
- добавлен Nginx gateway для проксирования API и раздачи статики/media;
- настроены Docker volumes `pg_data`, `static`, `media`;
- настроен локальный запуск через `docker-compose.yml`;
- настроен production-запуск через `docker-compose.production.yml`;
- подготовлен `.env.example`;
- настроен GitHub Actions workflow;
- добавлена публикация Docker-образов на Docker Hub;
- настроен автоматический деплой на удалённый сервер;
- добавлено Telegram-уведомление после успешного деплоя.

---

## Автор

Николь Журбенко  
GitHub: [kindarufy](https://github.com/kindarufy)

---

## Статус проекта

Проект выполнен в рамках курса **Python-разработчик** от Яндекс Практикума.

Основная цель проекта - освоить контейнеризацию, настройку Docker Compose, работу с PostgreSQL в контейнерах, настройку Nginx gateway и автоматизацию CI/CD-процесса через GitHub Actions.
