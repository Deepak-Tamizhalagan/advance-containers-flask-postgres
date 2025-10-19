# --- Build stage (optional if you add tooling later) ---
FROM python:3.13-slim AS runtime

# system deps (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# set workdir
WORKDIR /app

# copy only requirements first for layer caching
COPY app/requirements.txt ./app/requirements.txt
RUN pip install --no-cache-dir -r app/requirements.txt

# copy app code
COPY app ./app

# create non-root user & ensure logs path is writable
RUN useradd -u 10001 -m appuser \
  && mkdir -p /app/app/logs \
  && chown -R appuser:appuser /app

USER appuser

# expose app port (informational)
ENV PORT=8000
EXPOSE 8000

# run with gunicorn in container
# NOTE: module path is "app.app:app" (folder "app", file "app.py", object "app")
CMD ["gunicorn", "-b", "0.0.0.0:8000", "-w", "2", "app.app:app"]
