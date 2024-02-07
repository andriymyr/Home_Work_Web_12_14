# Встановлення базового образу Python
FROM python:3.11-slim

# Встановлення залежностей проекту та створення віртуального середовища Python
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
RUN pip install uvicorn
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install --yes gcc libc-dev make libffi-dev
RUN apt-get install
RUN pip install poetry
RUN uvicorn myapp:app

# Додавання всього іншого в проект
COPY .  /app

# Вказання команди запуску додатку
entrypoint ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
