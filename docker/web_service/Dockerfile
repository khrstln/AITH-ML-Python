# ------------------------------- Builder Stage ------------------------------- #
FROM python:3.11-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.4
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.in-project true && \
    poetry install --no-root --only main

# ------------------------------- Production Stage ---------------------------- #
FROM python:3.11-slim-bookworm AS production

WORKDIR /app

COPY /src src
COPY /db db
COPY /configs configs
COPY --from=builder /app/.venv .venv

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "src.web_service.app:app", "--host", "0.0.0.0", "--port", "8000"]
