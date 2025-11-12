# Use an official Python image.
FROM python:3.11-slim

# Set the working directory inside the container.
WORKDIR /app

# Copy over the Python dependencies.
COPY requirements.txt .

# Install the dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code.
COPY . .

# Start the Flask application.
CMD ["python", "app.py"]
