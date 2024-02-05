# Use an official Python runtime as a parent image
FROM python:3.11-alpine

# Set the working directory in the container
WORKDIR /app

# Create a non-root user
RUN adduser -D -u 1000 appuser

# Copy required contents into the container at /app
COPY mqtt_publisher_app /app

# Change the ownership of the working directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to the non-root user
USER appuser

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./entrypoint.sh .

# # Run publish when the container launches
# CMD ["python", "/app/publish.py"]
