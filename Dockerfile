FROM python:3.10-slim

RUN useradd -m flask
RUN pip install poetry

USER flask

WORKDIR /home/flask/app
COPY --chown=flask:flask . .

ENV PATH="/home/flask/.local/bin:$PATH"

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME='/home/flask/.local'

USER root 

RUN pip install cryptography
RUN mkdir -p /usr/local/lib/python3.10/site-packages /usr/local/bin && \
    chown -R flask:flask /usr/local/lib/python3.10/site-packages /usr/local/bin

USER flask

RUN poetry install --only main --no-interaction --no-root

CMD [ "python3", "-m" , "flask", "run","--host=0.0.0.0"]

EXPOSE 5000
