ARG PYTHON_VERSION=3.11.4

FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

ARG UID=10001

RUN adduser --disabled-password --gecos "" --home "/home/appuser" --shell "/sbin/nologin" --uid "${UID}" appuser

RUN --mount=type=cache,target=/root/.cache/pip --mount=type=bind,source=requirements.txt,target=requirements.txt python -m pip install -r requirements.txt

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

RUN mkdir -p /app/.pytest_cache && \
    chown -R appuser:appuser /app && \
    chmod -R 755 /app

USER appuser

COPY --chown=appuser:appuser . .

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0"]