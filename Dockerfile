# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости (для PostgreSQL)
RUN apt-get update && apt-get install -y gcc libpq-dev

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
