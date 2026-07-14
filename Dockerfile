ARG PYTHON_IMAGE=python:3.12-slim
FROM ${PYTHON_IMAGE}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml README.md reader3.py server.py ./
COPY templates ./templates
ARG PIP_INDEX_URL=https://pypi.org/simple
RUN pip install --no-cache-dir --timeout 120 --index-url "${PIP_INDEX_URL}" \
    "beautifulsoup4==4.14.2" \
    "ebooklib==0.20" \
    "fastapi==0.121.2" \
    "httpx==0.28.1" \
    "jinja2==3.1.6" \
    "python-multipart==0.0.27" \
    "uvicorn==0.38.0"

RUN mkdir -p /app/book && chown -R 1000:1000 /app
USER 1000:1000

EXPOSE 8123

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8123"]
