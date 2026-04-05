FROM python:3.10

WORKDIR /app

COPY server/ ./server
COPY inference.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]