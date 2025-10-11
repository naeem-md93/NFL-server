# Use the official Python image
FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y python3-dev python3-venv

# Set the working directory
WORKDIR /app

COPY requirements.txt ./
COPY . ./

# Install Python dependencies
RUN python3 -m venv .venv
ENV PATH=".venv/bin:$PATH"
RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose port 8000 for the application
EXPOSE 8000

# Run the Django application
CMD ["gunicorn", "base.wsgi:application", "--bind", "0.0.0.0:8000"]
