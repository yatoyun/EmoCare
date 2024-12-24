FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY ./backend/requirements.txt .
COPY ./backend/requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

# Copy project files
COPY . .

# as tty bash
CMD ["bash", "-i", "-l"]