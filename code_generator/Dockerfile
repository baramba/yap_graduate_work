FROM python:3.10.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
ENV REDIS_HOST=redis
ENV POSTGRES_SERVER=postgres
ENV FLASK_APP=main_flask.py
ENV DEBUG=True
ENV HOST_FLASK=localhost


RUN groupadd --system app && useradd --home-dir /app --system -g app app && chown app:app -R /app

RUN pip install -U pip wheel
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
USER app
COPY src/ .

#EXPOSE 5000
RUN celery -A main_flask.celery worker --loglevel=info --detach

#CMD ["python3", "-m", "flask", "run"]
CMD ["python3", "main_flask.py"]