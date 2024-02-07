FROM python:3.10-slim

RUN apt-get update \
    && apt-get install --no-cache --virtual .build-deps \
        gcc \
        libc-dev \
        make \
        libffi-dev \
    && pip install poetry

# Копіюємо файли проекту
COPY . /app

# Задаємо робочу директорію
WORKDIR /app

# Встановлюємо залежності через poetry
RUN poetry install --no-dev --no-interaction --no-ansi

# Виконуємо команду для запуску сервера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
