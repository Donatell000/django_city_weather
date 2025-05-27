FROM python:3.11.6-slim-bookworm
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /usr/src
COPY ./requirements.txt .

RUN apt update --allow-unauthenticated
RUN apt upgrade -y
RUN apt install --no-install-recommends --no-install-suggests -y python3-dev libpq-dev gcc netcat-traditional gettext\
    && apt install mc -y \
    && apt install procps -y \
    && python -m pip install --upgrade pip \
    && pip3 install -r requirements.txt \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

COPY ./app ./app
