FROM python:3.12.1-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH"

COPY ".python-version" "pyproject.toml" "uv.lock" ./

RUN uv sync --locked

COPY "predict.py" "xg_model.pkl" "dv.pkl" "app.py" "start.sh" ./

RUN chmod +x start.sh

EXPOSE 9696
EXPOSE 8501

ENTRYPOINT ["./start.sh"]