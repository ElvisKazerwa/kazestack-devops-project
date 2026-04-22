FROM python:3.9-slim

WORKDIR /app

COPY app/src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/src/ .

EXPOSE 5000

CMD ["python", "app.py"]
