FROM python:3.11-slim

WORKDIR /src

COPY boiler_telegram_bot/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/tg_logs

# Запуск бота
CMD ["python", "-m", "boiler_telegram_bot.bot"]