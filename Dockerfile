FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY app/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app ./app

# Copy and make start script executable
COPY start.sh .
RUN chmod +x start.sh

# Expose port
EXPOSE 8000

# Run FastAPI with start script
CMD ["./start.sh"]
