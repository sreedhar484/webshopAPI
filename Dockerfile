# Use the official Python image
FROM python:3.10


# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project
COPY . /app/

# Set Python path to ensure Django can find "webshop"
ENV PYTHONPATH="/app"

# Expose the port
EXPOSE 8000

# Start Django using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "webshop.wsgi:application"]
