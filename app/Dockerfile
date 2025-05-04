FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root
COPY . .

ENV APP_CONFIG__RUN__PORT=${APP_CONFIG__RUN__PORT}
ENV APP_CONFIG__RUN__ADDRESS=${APP_CONFIG__RUN__ADDRESS}
ENV APP_CONFIG__RUN__DISABLE_DOCS=${APP_CONFIG__RUN__DISABLE_DOCS}

EXPOSE ${APP_CONFIG__RUN__PORT}

CMD ["sh", "-c", "uvicorn main:app --host $APP_CONFIG__RUN__ADDRESS --port $APP_CONFIG__RUN__PORT"]