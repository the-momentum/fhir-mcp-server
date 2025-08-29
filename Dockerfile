FROM python:3.13-slim AS builder

RUN apt-get update && \
  apt-get install -y --no-install-recommends build-essential && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir --upgrade pyopenssl

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /root_project

COPY uv.lock pyproject.toml ./
COPY . .

RUN uv venv /root_project/.venv
ENV PATH="/root_project/.venv/bin:$PATH"
RUN uv sync --frozen --no-dev

FROM python:3.13-slim

RUN apt-get update && \
  apt-get install -y --no-install-recommends && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /root_project

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY --from=builder /root_project /root_project

ENV TRANSPORT_MODE=stdio

EXPOSE 8000

RUN uv run python scripts/start/load_models.py

CMD ["uv", "run", "python", "start.py", "--transport", "$TRANSPORT_MODE"]
