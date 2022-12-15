FROM python:3.10-slim as common

WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv /app/env \
    && /app/env/bin/pip install -r requirements.txt

COPY . .

EXPOSE 5000
RUN apt update && apt install -y curl
CMD ["/app/env/bin/gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
