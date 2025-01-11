# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/app/.venv/bin:/root/.local/bin:$PATH"

# Copy the project files into the container
COPY ./pyproject.toml ./poetry.lock ./requirements.txt /app/

# Install Python Dependencies
RUN poetry install --no-root

# Copy the rest of the Django project into the app directory
COPY . /app

# Expose the port your Django app runs on (default port 8000)
EXPOSE 8002

# Command to run Django app with Gunicorn
CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:8002", "quote_django.wsgi:application"]