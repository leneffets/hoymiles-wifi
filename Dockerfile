FROM python:3.12

# Set the working directory
WORKDIR /workspace

ENV PYTHONWARNINGS="ignore"
ENV IPADDR="192.168.1.184"
ENV TZ="Europe/Berlin"

# Install any dependencies
COPY requirements.txt ./
RUN apt update \
    && apt install -y librrd-dev \
    && pip install --no-cache-dir -r requirements.txt

# Create a directory for persistent data
RUN mkdir -p /workspace/data

# Copy the rest of the application code
COPY . .

# Set the default command to bash
CMD ["python3", "main.py"]
