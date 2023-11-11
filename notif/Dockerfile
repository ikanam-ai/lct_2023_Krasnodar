FROM python:3.10.4-slim-buster AS development_build

ENV NOTIF_PORT="1338"
ENV ADMIN_NOTIF_PSWD=""
ENV NOTIF_PSWD=""


RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock /app/
COPY notif/ /app/notif
RUN poetry install
ENTRYPOINT ["poetry", "run", "start"]
