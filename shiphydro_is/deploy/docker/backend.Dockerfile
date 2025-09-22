FROM python:3.11-slim AS base
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY backend/pyproject.toml backend/README.md /app/
RUN pip install --no-cache-dir .[dev]
COPY backend /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
