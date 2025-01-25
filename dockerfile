
FROM python:3.12-slim
ENV PIP_NO_CACHE_DIR=false

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY src/ .

EXPOSE 8080

CMD ["python", "main.py"]
