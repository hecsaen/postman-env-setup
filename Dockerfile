# Use a base image with Python installed
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the action files into the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install requests

RUN ls

# Specify the entry point for the action
ENTRYPOINT ["python", "src/action.py"]
