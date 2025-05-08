# # Stage 1: Frontend build
# FROM node:20 AS frontend-builder
# WORKDIR /app/frontend

# # Copy generated frontend scaffold (including vite.config.js, tailwind.config.cjs, src/)
# COPY frontend/ ./

# RUN npm ci
# RUN npm run build

# Stage 1: Frontend build
FROM node:20 AS frontend-builder
WORKDIR /app/frontend

# Copy only package.json first to generate lock file
COPY frontend/package.json ./

# Install deps & generate package-lock.json
RUN npm install

# Copy the rest of the frontend source
COPY frontend/ ./

# Build the frontend
RUN npm run build

# Stage 2: Backend build
FROM python:3.11-slim AS backend-builder
WORKDIR /app/backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/ .


# Stage 3: Final image
FROM python:3.11-slim
WORKDIR /app
# Copy backend
COPY --from=backend-builder /app/backend /app/backend
# Copy frontend static assets
COPY --from=frontend-builder /app/frontend/dist /app/static
# Copy .env example (ensure it's in project root)
COPY ./.env ./

EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]