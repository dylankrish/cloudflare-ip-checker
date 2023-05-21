# Use an appropriate base image, depending on your application's requirements
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the contents of your repository to the working directory in the container
COPY . .

# Install any necessary dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the entry point for the container
ENTRYPOINT ["python", "main.py"]

