FROM python:3.10.4-slim-buster AS development_build

ENV RABBITMQ_HOST=""
ENV RABBITMQ_PORT=3870
ENV RABBITMQ_USER=""
ENV RABBITMQ_PASSWORD=""
ENV RABBITMQ_VHOST="/"
ENV EXCHANGE_NAME=""
ENV DEQUE_NAME=""
ENV BINDING_KEY=""
ENV MONGO_HOST=""
ENV MONGO_PORT=""
ENV MONGO_USERNAME=""
ENV MONGO_PASSWORD=""
ENV MODEL_PATH=""
ENV PROCESSES=0
ENV NOTIF_URL=""
ENV ADMIN_NOTIF_PSWD=""

RUN apt-get -y update && apt-get -y upgrade && apt-get install -y ffmpeg
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
COPY worker/ /app/worker
RUN poetry install
ENTRYPOINT ["poetry", "run", "start"]