FROM python:3.11.2-slim-buster

WORKDIR /app

ARG UID=1000
ARG GID=1000

RUN apt-get update \
    && apt-get install -qq --no-install-recommends libpq-dev ncat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/* /usr/share/man/* \
    && groupadd -g ${GID} python \
    && useradd --create-home --no-log-init -u "${UID}" -g "${GID}" python \
    && mkdir -p /app \
    && chown -R python:python /app

COPY --chown=python:python . /app
RUN chmod --recursive +x /app/bin/ \
    && /app/bin/pip3-install.sh

USER python

WORKDIR /app/src
