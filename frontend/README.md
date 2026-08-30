# Фронтенд Плюс Дизайн

Сайт-визитка: витрина портфолио, о себе, форма заявки и админка работ.

```bash
npm install
npm run dev
```

Vite проксирует `/api` и `/media` на `http://localhost:8000`. В Docker Dev
цель прокси задаётся `VITE_API_PROXY`. Production-сборка (`npm run build`)
отдаётся nginx с того же origin, что и API.

Админка: `/admin/login`. JWT хранится в `sessionStorage`.
