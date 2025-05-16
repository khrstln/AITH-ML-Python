# ------------------------------ Builder Stage ------------------------------ #
FROM python:3.11-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 - && \
    ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

ENV POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

WORKDIR /app

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root --only main

# ----------------------------- Production Stage ----------------------------- #
FROM python:3.11-slim-bookworm AS production

WORKDIR /app

COPY --from=builder /app/.venv .venv
COPY /src src
COPY /models_sources models_sources

ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "src.model_service.main"]
