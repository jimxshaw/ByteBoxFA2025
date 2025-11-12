# Use an official Python image.
FROM python:3.11-slim

# Set the working directory inside the container.
WORKDIR /app

# Set Flask environment variable.
ENV FLASK_ENV=development

# Copy over the Python dependencies.
COPY requirements.txt .

# Install the dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code.
COPY . .

# Update the permissions of the shell script.
RUN chmod +x entrypoint.sh

# Start the Flask application.
CMD ["sh", "entrypoint.sh"]
