# Базовий образ
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

# Статичні файли та міграції
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Render використовує порт через $PORT
CMD ["gunicorn", "skin_shop.wsgi:application", "--bind", "0.0.0.0:${PORT}"]
