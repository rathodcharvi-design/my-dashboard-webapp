FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code + static assets
COPY app ./app

# Expose port for documentation
EXPOSE 8080

# Run Flask app
CMD ["python", "app/app.py"]

