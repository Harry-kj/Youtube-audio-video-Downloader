# Use official Python image
FROM python:3.11-slim

# Install ffmpeg and other dependencies
RUN apt-get update && apt-get install -y ffmpeg curl && apt-get clean

# Set work directory
WORKDIR /app

# Copy everything to container
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set environment variable to use ffmpeg inside your app
ENV RENDER=true

# Expose the port Flask runs on
EXPOSE 10000

# Start the app
CMD ["python", "app.py"]
