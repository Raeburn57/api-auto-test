import pymysql
from common.global_config import GLOBAL_CONFIG

class DBUtil:
    _conn = None
    @classmethod
    def _db_connect(cls):
        if cls._conn is None:
            cls._conn =  pymysql.connect(
                host = GLOBAL_CONFIG["db_host"],
                port = GLOBAL_CONFIG["db_port"],
                user = GLOBAL_CONFIG["db_user"],
                passwd = GLOBAL_CONFIG["db_password"],
                cursorclass = pymysql.cursors.DictCursor,
                charset = "utf8mb4"
            )
        return cls._conn

    @classmethod
    def db_query_one(cls, sql:str):
        conn = cls._db_connect()
        cursor = conn.cursor()

        try:
            cursor.execute(sql)
            return cursor.fetchone()
        finally:
            cursor.close()

    @classmethod
    def db_close(cls):
        if cls._conn is not None:
            cls._conn.close()
            cls._conn = None

