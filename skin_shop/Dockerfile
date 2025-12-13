FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Системні пакети
RUN apt-get update && apt-get install -y gcc \
    && rm -rf /var/lib/apt/lists/*

# Python залежності
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо проект
COPY . /app/

# Тільки збираємо статику (без міграцій!)
RUN python manage.py collectstatic --noinput

# Використовуємо shell для підстановки $PORT
CMD python manage.py migrate && gunicorn skin_shop.wsgi:application --bind 0.0.0.0:$PORT