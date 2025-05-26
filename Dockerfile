# Use official Python image
FROM python:3.11-slim

# Install ffmpeg and other needed packages
RUN apt-get update && apt-get install -y ffmpeg curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port 10000 and start the Flask app
EXPOSE 10000
CMD ["python", "app.py"]
