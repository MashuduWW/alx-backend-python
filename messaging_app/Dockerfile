FROM python:3.10

# Prevents Python from writing .pyc files and buffers output (helpful for logs)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY Requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r Requirements.txt

# Copy all project files into the container
COPY . /app/

# Expose Django's default port
EXPOSE 8000

# Run Django development server on 0.0.0.0:8000 so it listens externally
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
