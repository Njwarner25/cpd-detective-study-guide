FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

# Copy source code (excluding .env files via .dockerignore)
COPY . .

# Set environment variable for build
ARG EXPO_PUBLIC_BACKEND_URL
ENV EXPO_PUBLIC_BACKEND_URL=${EXPO_PUBLIC_BACKEND_URL}

# Build the web app with environment variables
RUN npx expo export --platform web

# Install serve to host the static files
RUN npm install -g serve

# Expose port (Railway dynamically assigns PORT)
EXPOSE 3000

# Serve the web build - use Railway's PORT env var or default to 3000
CMD sh -c "serve -s dist -l tcp://0.0.0.0:${PORT:-3000}"
# Force rebuild 1738202342

