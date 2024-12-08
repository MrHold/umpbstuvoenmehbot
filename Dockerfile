FROM python:3.10-slim

WORKDIR /app
ENV PYTHONPATH=/app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED=1
CMD ["python", "src/bot.py"]
