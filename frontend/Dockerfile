FROM node:20-slim

WORKDIR /app

# Install dependencies
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

# Copy source code
COPY . .

# Build the web app
RUN npx expo export --platform web

# Install serve to host the static files
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Serve the web build
CMD ["serve", "-s", "dist", "-l", "3000"]
