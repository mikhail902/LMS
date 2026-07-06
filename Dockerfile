FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . .

COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

EXPOSE 8000