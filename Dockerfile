FROM python:3.10-slim
WORKDIR /app
RUN apt-get update && apt-get install -y git curl build-essential
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/root/.local'

COPY . /app
RUN poetry install --no-root
EXPOSE 5000
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]
