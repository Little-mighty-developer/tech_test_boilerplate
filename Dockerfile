FROM python:3.11-slim

WORKDIR /app

# Create non-root user and install dependencies
RUN useradd -m appuser \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD ["curl", "-f", "http://localhost:8000/health"]

# Run pre-commit install
RUN pre-commit install

# Command to run the application
CMD ["python", "-m", "pytest"]