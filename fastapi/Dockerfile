FROM python:3.10.8-alpine

RUN apk update && apk add build-base && apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src /app

EXPOSE 8000

WORKDIR /app

ENTRYPOINT ["gunicorn", "main:app", "-b", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "-w", "1"]