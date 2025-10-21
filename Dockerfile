# Use official Python image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose the dynamic Render port
EXPOSE $PORT

# Start Gunicorn using Render's provided $PORT
CMD ["sh", "-c", "gunicorn core.wsgi:application --bind 0.0.0.0:${PORT}"]
