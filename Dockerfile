FROM python:3.12-slim
WORKDIR /app
COPY app.py .
RUN pip install --default-timeout=100 -i https://mirrors.aliyun.com/pypi/simple/ fastapi uvicorn psycopg2-binary
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
