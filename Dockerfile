FROM python:3.11-slim

WORKDIR /app

# Copy pip configuration for emergentintegrations
COPY backend/pip.conf /etc/pip.conf

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD uvicorn server:app --host 0.0.0.0 --port ${PORT:-8001}
