FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем entrypoint.sh отдельно, чтобы точно знать, где он лежит
COPY entrypoint.sh /app/entrypoint.sh

# Копируем остальной проект
COPY . .

# Делаем entrypoint исполняемым
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]