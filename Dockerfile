FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir \
    "a2a-sdk[http-server]>=0.3.0" \
    httpx>=0.28.1 \
    openai>=1.57.0 \
    pydantic>=2.11.4 \
    python-dotenv>=1.1.0 \
    uvicorn>=0.34.2 \
    requests>=2.31.0 \
    beautifulsoup4>=4.12.0 \
    langdetect>=1.0.9 \
    googletrans>=4.0.0

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "-m", "src"]
