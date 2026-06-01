FROM python:3.9

# Install docker CLI and build dependencies
RUN apt-get update && apt-get install -y \
    curl \
    gcc \
    python3-dev \
    libffi-dev \
    && curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh && \
    rm get-docker.sh

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# We'll run in the context of the project root when in docker-compose
# but the code will be in /app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
