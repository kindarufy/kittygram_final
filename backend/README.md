# Kittygram backend

Backend использует PostgreSQL. Полный запуск с БД и React описан
в [корневом README](../README.md); отдельно клонировать учебный шаблон не нужно.
Из корня репозитория после создания .env:

```bash
docker compose up -d --build
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py collectstatic --noinput
docker compose exec backend python manage.py createsuperuser
```

API: http://localhost:9000/api/, admin: http://localhost:9000/admin/.
Остановка: `docker compose down`.
