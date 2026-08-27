# README.MD для plusdesign

## О проекте

**Плюс Дизайн** — сайт-визитка дизайнера интерьера **Анастасии Плюсниной**.
Задача сайта: показать портфолио и принимать заявки на проекты.

Анастасия Плюснина — дизайнер-проектировщик и дизайнер-визуализатор
с опытом работы 4 года. Основная практика — интерьеры квартир и домов,
включая авторский надзор.

Japandi в этом проекте — **только визуальный стиль интерфейса**
(спокойная палитра, мало шума). Это не направление интерьеров и не
описание услуг. Подробности UI — в `docs/fronted.md`.

## Дополнительные ресурсы:
дополнительные материалы и документация доступны в папке `docs/` репозитория.

- `docs/api.md` — контракт HTTP API
- `docs/fronted.md` — визуальный стиль и требования к UI
- `docs/decisions.md` — журнал архитектурных решений
- `AGENTS.md` — правила работы для ИИ-агентов

## Текущее состояние

Реализованы бэкенд первой итерации и публичный фронтенд сайта-визитки:
витрина портфолио с пагинацией и форма-заявка на проект интерьера.

| Компонент | Статус |
| --- | --- |
| FastAPI-приложение, конфиг, логирование, обработка ошибок | готово |
| PostgreSQL + SQLAlchemy 2.0 async + Alembic | готово |
| `GET /api/v1/portfolio` — список с пагинацией | готово |
| `GET /api/v1/portfolio/{slug}` — одна работа | готово |
| `POST /api/v1/portfolio` — создание работы | готово, без авторизации |
| `POST /api/v1/leads` — форма-заявка | готово |
| Тесты (pytest, 18 шт.) | готово |
| Фронтенд React + TypeScript (визитка, локальный запуск) | готов |
| Авторизация и админка | не начаты |

## Стек

- **Бэкенд:** Python 3.11+, FastAPI, SQLAlchemy 2.0 (async), asyncpg, Alembic, Pydantic v2
- **База данных:** PostgreSQL 16
- **Тесты:** pytest, pytest-asyncio, httpx
- **Линт:** ruff
- **Фронтенд:** React + TypeScript, Vite, локально `http://localhost:5173`

## Быстрый старт

```bash
cd backend

# 1. Поднять PostgreSQL
docker compose up -d db

# 2. Окружение и зависимости
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

# 3. Настройки
cp .env.example .env

# 4. Миграции
alembic upgrade head

# 5. Запуск
uvicorn app.main:app --reload
```

Документация API поднимется на http://localhost:8000/docs

Фронтенд (проксирует `/api` на бэкенд):

```bash
cd frontend
npm install
npm run dev
```

### Полезные команды

```bash
cd backend

pytest                        # тесты (по умолчанию на SQLite в памяти)
ruff check .                  # линт
ruff check --fix .            # линт с автоисправлением
alembic revision --autogenerate -m "описание"   # новая миграция
alembic downgrade -1          # откатить последнюю миграцию
alembic upgrade head --sql    # посмотреть SQL без применения
```

Чтобы прогнать тесты на реальном PostgreSQL, задайте `TEST_DATABASE_URL`
с драйвером asyncpg и отдельной базой.

## Архитектура бэкенда

Слои и направление зависимостей — строго внутрь:

```
endpoints  →  services  →  repositories  →  models
   (HTTP)     (домен)      (SQLAlchemy)      (БД)
```

- **`endpoints/`** знает про HTTP, но не про SQLAlchemy: разбирает запрос,
  зовёт сервис, отдаёт Pydantic-схему.
- **`services/`** содержит бизнес-правила и не импортирует FastAPI. Зависимость
  от хранилища описана через `typing.Protocol`, поэтому сервис не привязан к
  конкретному репозиторию и легко тестируется на заглушке.
- **`repositories/`** — единственное место, где живут запросы к БД.
- **`core/exceptions.py`** — доменные исключения. Транспортный слой
  переводит их в HTTP-коды обработчиками в `app/main.py`.

Границы транзакции задаёт зависимость `get_db`: один запрос — одна транзакция,
коммит на успехе, откат на исключении. Репозитории делают только `flush`.

## Структура репозитория:
```
plusdesign/
├── README.md
├── AGENTS.md
├── docs/
│   ├── api.md                       # контракт HTTP API
│   ├── fronted.md                   # стиль и требования к UI
│   └── decisions.md                 # журнал решений
│
├── frontend/                        # React + TypeScript, сайт-визитка
│
└── backend/
    ├── app/
    │   ├── __init__.py
    │   ├── main.py                  # точка входа FastAPI, CORS, обработчики ошибок
    │   ├── config.py                # настройки, env-переменные, pydantic-settings
    │   ├── dependencies.py          # общие зависимости: get_db, пагинация
    │   │
    │   ├── core/
    │   │   ├── __init__.py
    │   │   ├── exceptions.py        # доменные исключения
    │   │   └── logging.py           # настройка логирования
    │   │   # security.py            # JWT и хэширование — когда появится авторизация
    │   │
    │   ├── db/
    │   │   ├── __init__.py
    │   │   ├── base.py              # Base, TimestampMixin
    │   │   ├── session.py           # async engine, фабрика сессий
    │   │   └── migrations/          # alembic-миграции
    │   │       ├── env.py
    │   │       ├── script.py.mako
    │   │       └── versions/
    │   │           └── 0001_init.py
    │   │
    │   ├── models/
    │   │   ├── __init__.py          # регистрирует модели в Base.metadata
    │   │   ├── portfolio.py         # PortfolioItem
    │   │   └── lead.py              # Lead, LeadStatus
    │   │
    │   ├── schemas/
    │   │   ├── __init__.py
    │   │   ├── common.py            # Page, PaginationParams, ErrorResponse
    │   │   ├── portfolio.py         # схемы работ портфолио
    │   │   └── lead.py              # схемы заявки, нормализация телефона
    │   │
    │   ├── api/
    │   │   ├── __init__.py
    │   │   ├── deps.py              # сборка сервисов из репозиториев
    │   │   └── v1/
    │   │       ├── __init__.py
    │   │       ├── router.py        # агрегирующий роутер для /api/v1
    │   │       └── endpoints/
    │   │           ├── __init__.py
    │   │           ├── health.py    # healthcheck
    │   │           ├── portfolio.py # витрина портфолио
    │   │           └── leads.py     # форма-заявка
    │   │
    │   ├── services/
    │   │   ├── __init__.py
    │   │   ├── portfolio_service.py # бизнес-логика портфолио
    │   │   └── lead_service.py      # бизнес-логика заявок
    │   │
    │   ├── repositories/
    │   │   ├── __init__.py
    │   │   ├── base.py              # общий CRUD над сессией
    │   │   ├── portfolio_repo.py    # запросы по работам портфолио
    │   │   └── lead_repo.py         # запросы по заявкам
    │   │
    │   └── utils/
    │       ├── __init__.py
    │       └── pagination.py        # offset/limit и подсчёт количества
    │
    ├── tests/
    │   ├── __init__.py
    │   ├── conftest.py              # фикстуры pytest, тестовый клиент, тестовая БД
    │   ├── test_health.py
    │   ├── test_portfolio.py
    │   └── test_leads.py
    │
    ├── alembic.ini                  # конфиг Alembic
    ├── docker-compose.yml           # PostgreSQL для локальной разработки
    ├── pyproject.toml               # зависимости, ruff, pytest
    ├── requirements.txt             # рантайм-зависимости
    ├── requirements-dev.txt         # зависимости для разработки и тестов
    └── .env.example                 # пример переменных окружения
```

## Что дальше

- Категории и теги работ, фильтрация в списке портфолио
- Галерея изображений для работы (сейчас одна обложка)
- Флаги `is_published` и `sort_order` для управления витриной
- Авторизация и админка, закрытие `POST /api/v1/portfolio`
- Уведомление о новой заявке (почта или мессенджер)
