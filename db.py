import psycopg2
import logging
from functools import wraps
import configparser
import traceback

logger = logging.getLogger(__name__)


config = configparser.ConfigParser()
config.read("config.ini")
connection_pool = psycopg2.pool.SimpleConnectionPool(config['db']['min_conn'], 
                                                        config['db']['max_conn'], 
                                                        user=config['db']['user'],
                                                        password=config['db']['password'],
                                                        host=config['db']['host'],
                                                        port=config['db']['port'],
                                                        database=config['db']['database'])

def empty_tables():
    conn = connection_pool.getconn()       
    cursor = conn.cursor() 
    cursor.execute("TRUNCATE TABLE inverter;")
    cursor.execute("TRUNCATE TABLE home_consumption;")
    cursor.execute("TRUNCATE TABLE pv_generator;")
    conn.commit()
    cursor.close()
    connection_pool.putconn(conn)


def with_cursor(write=False):
    def with_cursor_decorator(func):
        @wraps(func)
        def with_cursor_wrapper(*args, **kwargs):
            conn = connection_pool.getconn()       
            cursor = conn.cursor(cursor_factory=psycopg2.extras.NamedTupleCursor)     
            try:
                result = func(*args, connection=conn, cursor=cursor, **kwargs)
            except Exception as e:                
                logger.error("SQL command failed")
                logger.error(traceback.format_exc())
                if write:
                    logger.info("Rollback")
                    conn.rollback()
                raise
            else:
                if write:
                    logger.debug("Commit")
                    conn.commit()
            finally:                
                cursor.close()
                logger.debug("Cursor closed")
                connection_pool.putconn(conn) 
                logger.debug("Connection back into the pool")               
            return result
        return with_cursor_wrapper
    return with_cursor_decorator