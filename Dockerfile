# Build stage
FROM python:3.12-slim AS builder

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends libpq5 && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Ensure instance directory exists for SQLite fallback
RUN mkdir -p /app/instance

ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

EXPOSE 8080

CMD ["gunicorn", "render_entry:app", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "120"]
