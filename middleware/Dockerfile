# Base image
FROM python:3.9-alpine
RUN pip install requests


# Set working directory
WORKDIR /middleware

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY .. .

# Expose port
EXPOSE 8080

# Start the app
CMD ["python3", "middleware.py"]