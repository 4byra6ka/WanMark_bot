FROM python:3.12-slim
ENV PYTHONUNBUFFERED 1
WORKDIR /app
#COPY pyproject.toml .
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
#COPY ./ ./
CMD ["sh", "-c", "sleep 20; celery -A config worker -l INFO"]