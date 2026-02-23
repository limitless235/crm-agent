# ---- Base image ----
FROM python:3.12-slim

# ---- System deps ----
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# ---- Workdir ----
WORKDIR /app

# ---- Python deps ----
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---- App code ----
COPY app ./app

ENV PYTHONPATH=/app

# ---- Runtime ----
EXPOSE 8000

CMD sh -c "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"
