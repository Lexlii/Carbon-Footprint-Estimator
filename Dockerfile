# Stage 1: Builder - compile dependencies
FROM python:3.12.1-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

COPY ".python-version" "pyproject.toml" "uv.lock" ./

RUN uv sync --locked --no-dev

# Stage 2: Runtime - minimal production image
FROM python:3.12.1-slim-bookworm

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy only the compiled venv from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application files
COPY "predict.py" "xg_model.pkl" "dv.pkl" "app.py" "start.sh" ./

RUN chmod +x start.sh

# Clean up pip cache and other non-essential files
RUN find /app/.venv -type d -name "tests" -exec rm -rf {} + 2>/dev/null || true && \
    find /app/.venv -type d -name "*.dist-info" -exec rm -rf {} + 2>/dev/null || true && \
    find /app/.venv -type f -name "*.pyc" -delete && \
    find /app/.venv -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

EXPOSE 9696
EXPOSE 8501

ENTRYPOINT ["./start.sh"]