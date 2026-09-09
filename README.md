# Kittygram Final

**Kittygram Final** — учебное Django + React приложение с PostgreSQL, Nginx, Docker Compose и GitHub Actions.

Функционально Kittygram — социальная сеть для публикации карточек котиков. Репозиторий в первую очередь демонстрирует инфраструктурную часть full-stack приложения: контейнеризацию, production configuration, автоматические проверки и deployment flow.

## Что демонстрирует проект

- контейнеризацию Django backend;
- контейнеризацию React frontend;
- отдельный Nginx gateway;
- PostgreSQL в отдельном контейнере;
- volumes для database, static и media;
- локальный и production compose-файлы;
- конфигурацию через `.env`;
- Gunicorn для backend;
- backend/frontend проверки в GitHub Actions;
- проверку сборки Docker images без production-секретов;
- отдельный ручной production deployment через SSH;
- migrations и collectstatic в deployment flow;
- Telegram notification после успешного deploy.

## Стек

**Backend:** Python, Django, Django REST Framework, Djoser, PostgreSQL, Gunicorn  
**Frontend:** JavaScript, React 17, React Router  
**Infrastructure:** Docker, Docker Compose, Nginx, Docker Hub, GitHub Actions, SSH

## Архитектура

```text
Client
  │
  ▼
Nginx gateway
  ├──► React static
  ├──► Django API / admin
  └──► media
          │
          ▼
      PostgreSQL
```

Контейнеры:

| Сервис | Назначение |
| --- | --- |
| `backend` | Django API и admin |
| `frontend` | сборка React SPA |
| `gateway` | Nginx routing/static/media |
| `db` | PostgreSQL |

## Интерфейс

![Kittygram — интерфейс приложения](docs/assets/kittygram-app.png)

## Структура

```text
kittygram_final/
├── backend/
├── frontend/
├── nginx/
├── .github/workflows/
│   ├── main.yml              # CI: tests + Docker build
│   └── deploy.yml            # manual production deployment
├── docker-compose.yml
├── docker-compose.production.yml
├── .env.example
└── README.md
```

## Локальный запуск

```bash
git clone https://github.com/nikamurkaa/kittygram_final.git
cd kittygram_final
cp .env.example .env
docker compose up -d --build
```

Пример локальных переменных находится в `.env.example`. Для реального deployment необходимо заменить `SECRET_KEY`, database password, `ALLOWED_HOSTS` и `CSRF_TRUSTED_ORIGINS`.

Интерфейс: http://localhost:9000/. Нужны Docker Engine/Desktop и Compose v2.
В PowerShell скопируйте шаблон командой `Copy-Item .env.example .env`.

После запуска примените migrations:

```bash
docker compose exec backend python manage.py migrate
```

Соберите backend static:

```bash
docker compose exec backend python manage.py collectstatic --noinput
```

Регистрация доступна через веб-интерфейс. Администратора создайте командой:

```bash
docker compose exec backend python manage.py createsuperuser
```

Остановка: `docker compose down` (данные в volumes сохраняются).

## CI/CD

`.github/workflows/main.yml` запускается на push и pull request в `main`. Он проверяет backend, frontend и сборку всех Docker images, не требуя production SSH/Docker Hub secrets.

`.github/workflows/deploy.yml` запускается вручную через `workflow_dispatch`. Он публикует Docker images и выполняет SSH deployment только когда production environment действительно настроен.

Такой split отделяет качество кода от доступности внешнего сервера: недоступный production host не делает обычный CI красным.

Deployment secrets хранятся в GitHub Actions Secrets и не должны попадать в repository files.

## Статус

Проект завершён в рамках курса **«Python-разработчик» Яндекс Практикума** и демонстрирует Docker, Django deployment, PostgreSQL, Nginx и CI/CD.

## Автор

[Николь Журбенко](https://github.com/nikamurkaa)
