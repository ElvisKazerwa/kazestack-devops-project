FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PORT=5000

WORKDIR /app

# Install dependencies first
COPY src/requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip && \
  python -m pip install --no-cache-dir -r requirements.txt

# Copy application source
COPY src/ .

USER nobody

EXPOSE 5000

CMD ["python", "app.py"]