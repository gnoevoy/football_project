FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt && \
    # Install browsers for Playwright
    playwright install --with-deps chromium

CMD [ "python", "scheduler.py"]