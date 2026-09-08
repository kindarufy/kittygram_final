# Kittygram frontend

React-интерфейс карточек котов. Для работы API, загрузки фото и авторизации
используйте Compose из [корневого README](../README.md).

```bash
# Из корня репозитория после создания .env
docker compose up -d --build
```

Примените миграции и соберите backend static по основной инструкции.
Откройте http://localhost:9000/.

Для отдельной проверки сборки нужен Node.js 22:

```bash
cd frontend
npm ci
npm run build
```

Standalone dev-server не заменяет полный Compose: запросам API нужен backend/gateway.
