## Stage 1: Build the dashboard
FROM node:20-alpine AS dashboard-build
WORKDIR /dashboard
COPY dashboard/package*.json ./
RUN npm ci
COPY dashboard/ .
RUN npm run build

## Stage 2: Python backend
FROM python:3.11-slim

WORKDIR /app

# Copy pip configuration for emergentintegrations
COPY backend/pip.conf /etc/pip.conf

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Copy built dashboard into backend static directory
COPY --from=dashboard-build /dashboard/dist ./static

CMD uvicorn server:app --host 0.0.0.0 --port ${PORT:-8001}
