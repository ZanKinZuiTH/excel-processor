# Use multi-stage build
FROM python:3.9-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create and set working directory
WORKDIR /build

# Copy only requirements first for better caching
COPY requirements.txt setup.py ./
COPY README.md ./

# Install dependencies
RUN pip install --no-cache-dir -e .

# Final stage
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_USER=appuser \
    APP_DIR=/app

# Create non-root user
RUN useradd --create-home $APP_USER

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Create necessary directories
RUN mkdir -p $APP_DIR/data $APP_DIR/templates $APP_DIR/logs $APP_DIR/dicom_files \
    && chown -R $APP_USER:$APP_USER $APP_DIR

# Set working directory
WORKDIR $APP_DIR

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /build/excel_processor.egg-info /usr/local/lib/python3.9/site-packages/excel_processor.egg-info

# Copy application code
COPY --chown=$APP_USER:$APP_USER . .

# Switch to non-root user
USER $APP_USER

# Create volume mount points
VOLUME ["$APP_DIR/data", "$APP_DIR/dicom_files", "$APP_DIR/logs"]

# Expose ports
EXPOSE 8000 8501

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start application with proper SSL configuration
CMD ["sh", "-c", "uvicorn api:app --host 0.0.0.0 --port 8000 --ssl-keyfile=/app/certs/key.pem --ssl-certfile=/app/certs/cert.pem & streamlit run ui.py"] 