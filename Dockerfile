FROM python:3.11-bookworm as builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONUSERBASE=/app/__pypackages__

COPY requirements.lock ./
RUN pip install --user --no-cache-dir -r requirements.lock

# https://github.com/GoogleContainerTools/distroless/blob/main/python3/BUILD
# distroless/python3-debian12のPythonは3.11
FROM gcr.io/distroless/python3-debian12:nonroot as runner
WORKDIR /app
ENV PYTHONUSERBASE=/app/__pypackages__

USER nonroot
COPY --from=builder /app/__pypackages__ /app/__pypackages__
COPY --chown=nonroot:nonroot . ./

CMD ["main.py"]
