FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PORT=5000

WORKDIR /app

# Copy and install dependencies first (better layer caching)
COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
  python -m pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ .

# Drop privileges
USER nobody

EXPOSE 5000

# Production WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]