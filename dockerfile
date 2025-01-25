ARG PLATFORM=linux/amd64
FROM --platform=$PLATFORM python:3.12-slim

ENV PIP_NO_CACHE_DIR=false
ENV PYTHONPATH=/app

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 8080

CMD ["python", "main.py"]
