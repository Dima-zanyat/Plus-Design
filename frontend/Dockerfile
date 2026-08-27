FROM node:22-alpine

WORKDIR /app

# Копируем файлы зависимостей
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем остальной код
COPY . .

# Открываем порт (замените на порт вашего фреймворка, например, 3000 для React/Next или 5173 для Vite)
EXPOSE 5173

# Команда запуска (замените dev на вашу команду из package.json, если она отличается)
CMD ["npm", "run", "dev"]
