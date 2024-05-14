FROM python:3.12-alpine

# Set the working directory
WORKDIR /app

# Install package dependencies
RUN apk add --no-cache \
    build-base \
    opus-dev \
    ffmpeg

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY src/ .

# Run the application
CMD ["python", "src/run.py"]