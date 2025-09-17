FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY conda.yaml .
RUN pip install conda-env-to-requirements && \
    conda-env-to-requirements conda.yaml > requirements.txt && \
    pip install -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY MLproject .

# Set environment variables
ENV PYTHONPATH=/app
ENV MLFLOW_TRACKING_URI=http://mlflow-service:80

# Default command
CMD ["python", "src/inference.py"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1
