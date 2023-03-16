import logging
import uuid

import psycopg2

from config.config import settings
class DataDjango:
    """Класс дял загрузки данных в Postgres"""
    query_read_data = f"""SELECT * FROM  content.bulk_creation WHERE id='%s'"""
    query_write_status = f"""UPDATE content.bulk_creation SET creation_done = %s, url_download = '%s' WHERE id = '%s'"""

    def __init__(self, pg_connect):
        self.pg_connect = pg_connect

    def read_data(self, id: uuid.UUID):
        """Получаем из БД юзера по имени"""
        try:
            query = self.query_read_data % id
            curpg = self.pg_connect.cursor()
            curpg.execute(query)
            self.data_param = curpg.fetchone()
        except psycopg2.DatabaseError as e:
            logging.critical("Error %s" % e)

    def change_status(self, id: uuid, path: str, status: bool = True):
        """Получаем из БД юзера по имени"""
        try:
            url_path = f"{settings.HOST}/api/v1/code_generator/{path.strip('./')} "
            query = self.query_write_status % (status, url_path, id)
            curpg = self.pg_connect.cursor()
            curpg.execute(query)
        except psycopg2.DatabaseError as e:
            logging.critical("Error %s" % e)
