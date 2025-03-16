FROM python:3.12

# Set the working directory
WORKDIR /workspace

ENV PYTHONWARNINGS="ignore"

# Install any dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the default command to bash
CMD ["bash"]
