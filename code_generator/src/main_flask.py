import logging
from datetime import datetime
from http import HTTPStatus

import psycopg2
from celery import Celery
from celery.bin import worker
from flask import Flask, send_file
from psycopg2.extras import DictCursor

from config.config import PostgresDsn
from core.django_reader import DataDjango
from core.main_script import script
from model import DataParam

dsn = PostgresDsn().dict()
app = Flask(__name__)
log = logging.getLogger(__name__)

app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])


@celery.task
def worker(id):
    log.info("Worker run with id: %s" % id)
    with psycopg2.connect(**dsn, cursor_factory=DictCursor) as pg_conn:
        dd = DataDjango(pg_conn)
        dd.read_data(id)
        data = dd.data_param
        datas = DataParam(title=data['title'],
                          description=data['description'],
                          start_at=data['start_at'],
                          expired=data['expired'],
                          activates_possible=1,
                          discount_type=data['discount_type'],
                          discount_amount=data['discount_amount'],
                          minimal_amount=data['minimal_amount'],
                          path=f'./download/{datetime.now().strftime("%Y-%m-%d %H:%M")}.csv',
                          created_by=data['created_by_id'],
                          count_codes=1
                          )
        with open(datas.path, 'w') as file:
            script(pg_conn, file, datas)
        dd.change_status(id, datas.path)
        log.info('Write filename: %s' % datas.path)


@app.route('/api/v1/code_generator/id/<string:id>')
def run(id):
    log.info('Flask get id: %s' % id)
    worker.delay(id)
    return "Success", HTTPStatus.OK


@app.route('/api/v1/code_generator/download/<string:path>')
def downloadFile(path):
    path_to_file = f'./download/{path}'
    return send_file(path_to_file, as_attachment=True)


if __name__ == "__main__":
    app.run(port=5000)
