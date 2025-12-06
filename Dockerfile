FROM python:3.11-slim

WORKDIR /app

# 1. Bog'liqliklarni o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. Entrypoint skriptini nusxalash va execute ruxsat berish
COPY ./deploy/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# 3. Loyiha fayllarini nusxalash
COPY . .

# 4. ENTRYPOINT va CMD
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]

EXPOSE 8000
