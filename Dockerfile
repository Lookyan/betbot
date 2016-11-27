FROM python:3.5.2-slim

WORKDIR /usr/src/app
ENV PYTHONPATH=/usr/src/app

COPY ./requirements.txt /usr/src/app/

RUN apt-get update \
    && apt-get install -y libpq-dev gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/*

COPY . /usr/src/app

CMD ["python3", "bin/bot.py"]
