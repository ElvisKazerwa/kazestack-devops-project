FROM python:3.11-slim

# Python runtime behavior
ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first (cache-friendly)
COPY requirements.txt .

RUN pip install --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run as non-root
USER nobody

EXPOSE 5000

CMD ["python", "app.py"]