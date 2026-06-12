# Suboptimal test solver — subnet112 scoring-pipeline validation.
FROM ghcr.io/subnet112/solver-base:v1

COPY requirements.txt /app/solver/requirements.txt
RUN pip install --no-cache-dir -r /app/solver/requirements.txt 2>/dev/null || true

COPY solver.py /app/solver/solver.py
# Base image provides the entrypoint; do NOT add CMD/ENTRYPOINT.
