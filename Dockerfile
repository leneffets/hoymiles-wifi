FROM python:3-slim

# Set the working directory
WORKDIR /workspace

ENV TZ="Europe/Berlin"

# Install any dependencies
COPY requirements.txt ./
RUN apt update \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /var/lib/apt/lists/*

# Create a directory for persistent data
RUN mkdir -p /workspace/data

# Copy the rest of the application code
COPY . .

# Set the default command to bash
CMD ["python3", "main.py"]
