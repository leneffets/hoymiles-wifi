FROM python:3.12

# Set the working directory
WORKDIR /workspace

ENV PYTHONWARNINGS="ignore"
ENV IPADDRESS="192.168.1.184"

# Install any dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the default command to bash
CMD ["python3", "main.py"]
