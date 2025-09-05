# 1. Python base image
FROM python:3.12-slim

# 2. Ishchi papka
WORKDIR /app

# 3. System kutubxonalarini o‘rnatish
RUN apt-get update && apt-get install -y libpq-dev gcc curl && rm -rf /var/lib/apt/lists/*

# 4. wait-for-it.sh ni yuklab olish va executable qilish
RUN curl -o wait-for-it.sh https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh
RUN chmod +x wait-for-it.sh

# 5. Dependencies o‘rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 6. Source code’ni nusxalash
COPY . .

# 7. Static fayllarni yig‘ish
RUN python manage.py collectstatic --noinput

# 8. Gunicorn orqali run qilish, DB tayyor bo‘lishini kutadi
CMD ["./wait-for-it.sh", "db:5432", "--", "gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
