import logging
import uuid
from datetime import datetime

import psycopg2

from model import DataParam


class PromocodesCreate:
    """Класс дял загрузки данных в Postgres"""
    QUERY_INSERT_CODE = f"""INSERT INTO content.promo (id, created, modified, title, description, code, start_at, expired, 
                                            activates_possible, activates_left, discount_type, discount_amount, minimal_amount,
                                            is_active, created_by_id )
                            VALUES """

    QUERY_INSERT_CODE_PRODUCT = f"""INSERT INTO content.product_promo (id, created, modified, product_id, promo_code_id) VALUES """
    arg_code_product = f"""('%s', '{datetime.now()}', '{datetime.now()}', '%s', '%s')"""

    def __init__(self,
                 pg_connect,
                 data: DataParam):
        self.uuids = list()
        self.pg_connect = pg_connect
        self.arg_code = f""" ('%s', 
                            '{datetime.now()}', 
                            '{datetime.now()}', 
                            '{data.title}', 
                            '{data.description}', 
                            '%s', 
                            '{data.start_at}', 
                            '{data.expired}', 
                            {data.activates_possible},
                            {data.activates_possible}, 
                            '{data.discount_type}', 
                            {data.discount_amount}, 
                            {data.minimal_amount},
                            {data.is_active}, 
                            {data.created_by})
                            """

    def write_code_to_db(self, records: list) -> None:
        """Метод загрузки данных

        Param
        records: список промокодов для загрузки"""
        try:
            curpg = self.pg_connect.cursor()
            args = ''
            for i in records:
                uuid_code = uuid.uuid4()
                self.uuids.append(uuid_code)
                args += ',' + (self.arg_code % (uuid_code, i))
            curpg.execute(self.QUERY_INSERT_CODE + args.strip(','))
        except psycopg2.DatabaseError as e:
            logging.critical("Error %s" % e)

    def write_code_usluga_to_db(self, products_id: list) -> None:
        """Запись в базу для связывания промокода с id услуги"""
        if products_id == None:
            return
        try:
            args = ''
            curpg = self.pg_connect.cursor()
            for i in products_id:
                for j in self.uuids:
                    args += ',' + (self.arg_code_product % (uuid.uuid4(), i, j))
            curpg.execute(self.QUERY_INSERT_CODE_PRODUCT + args.strip(','))
        except psycopg2.DatabaseError as e:
            logging.critical("Error %s" % e)