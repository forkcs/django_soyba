FROM python:3.12-alpine AS builder
WORKDIR /app

ENV GID=1000
ENV UID=1000

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
  uv sync --frozen --no-install-project --no-editable

COPY . .

RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv \
  uv sync --frozen --no-editable

FROM python:3.12-alpine as runner
COPY --from=builder --chown=app:app /app /app
WORKDIR /app

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /app/src

ENTRYPOINT [ "./celery-worker.sh" ]
