FROM python:3.11-slim-bullseye

WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем папку src
COPY src/ ./src/

# Команда запуска бота
CMD ["python", "-m", "src.bot"]

