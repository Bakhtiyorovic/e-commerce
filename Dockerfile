# Dockerfile misol
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# entrypoint.sh ga execute permission berish
RUN chmod +x /app/entrypoint.sh

# container ishga tushganda entrypoint.sh ishga tushadi
ENTRYPOINT ["/app/entrypoint.sh"]
