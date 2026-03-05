# Base image
FROM python:3.11-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ishchi katalog
WORKDIR /app

# Kerakli fayllarni ko‘chirish
COPY requirements.txt .

# System kutubxonalar va Python paketlarini o‘rnatish
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    curl \
 && pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && apt-get clean && rm -rf /var/lib/apt/lists/*

# Project fayllarini ko‘chirish
COPY . .

# Entrypoint scriptni tayyorlash
RUN sed -i 's/\r$//' /app/deploy/entrypoint.sh \
 && chmod +x /app/deploy/entrypoint.sh

# Entrypoint va default command
ENTRYPOINT ["/app/deploy/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60"]
