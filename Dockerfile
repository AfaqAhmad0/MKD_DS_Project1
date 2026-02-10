FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Hugging Face Spaces expects port 7860
ENV PORT=7860

# Run FastAPI app from app.py
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]

