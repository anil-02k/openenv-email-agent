FROM python:3.10-slim

WORKDIR /app

# Copy files
COPY server/ ./server
COPY inference.py .
COPY requirements.txt .
COPY pyproject.toml .
COPY uv.lock .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run app
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]