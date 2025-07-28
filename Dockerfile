# Use official Python 3.10 slim image
FROM python:3.10-slim

WORKDIR /app

# Copy your scripts and requirements file
COPY index.py ./
COPY extractor.py ./
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command: run index.py in /app, which reads input/*.pdf and writes output/*.json
CMD ["python", "index.py"]
