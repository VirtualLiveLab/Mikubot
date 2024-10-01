FROM python:3.11-bookworm as builder

WORKDIR /app
ENV UV_SYSTEM_PYTHON=true \
    UV_COMPILE_BYTECODE=1 \
    UV_CACHE_DIR=/root/.cache/uv \
    UV_LINK_MODE=copy

# Install dependencies
RUN --mount=from=ghcr.io/astral-sh/uv:0.4.17,source=/uv,target=/bin/uv \
    --mount=type=cache,target=${UV_CACHE_DIR} \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv export --frozen --no-dev --format requirements-txt > requirements.txt \
    && uv pip install -r requirements.txt --target /app/.uv-pip/site-packages

# https://github.com/GoogleContainerTools/distroless/blob/main/python3/BUILD
# distroless/python3-debian12のPythonは3.11
FROM gcr.io/distroless/python3-debian12:nonroot as runner
WORKDIR /app

# distrolessのPythonはデフォルトではsite-packagesを参照しない
ENV PYTHONPATH=/app/.uv-pip/site-packages

USER nonroot
COPY --from=builder /app/.uv-pip/site-packages /app/.uv-pip/site-packages
COPY --chown=nonroot:nonroot . ./

CMD ["main.py"]
