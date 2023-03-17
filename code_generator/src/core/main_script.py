import logging

import psycopg2
from model import DataParam
from psycopg2.extras import DictCursor
from core.code_create import PromocodesCreate
from core.str_generator import generate_random_str

from config.config import PostgresDsn, settings

log = logging.getLogger(__name__)
dsn = PostgresDsn().dict()
kol_code = 5
path = "./test.csv"

max_in_records_db = settings.MAX_IN_RECORDS_DB


def script(pg_conn, fl, data: DataParam):
    pg = PromocodesCreate(pg_conn, data)
    j = 0
    codes = list()
    for i in range(data.count_codes + 1):
        if (j == max_in_records_db) or (i == data.count_codes):
            pg.write_code_to_db(codes)
            for code in codes:
                fl.write(code + "\n")
            codes = list()
            j = 0

        codes.append(generate_random_str(8))
        j += 1
    pg.write_code_usluga_to_db(data.product_id)
    log.info('Коды сгенерированы')


def local_script(data):
    with psycopg2.connect(**dsn, cursor_factory=DictCursor) as pg_conn, open(path, 'w') as fl:
        script(pg_conn, fl, data)
