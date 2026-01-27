# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Railway sets PORT automatically
ENV PORT=8001

# Start command
CMD ["sh", "-c", "uvicorn server:app --host 0.0.0.0 --port $PORT"]
