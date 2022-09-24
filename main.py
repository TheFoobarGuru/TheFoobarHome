import db
import plenticore
import asyncio
import logging
from logging.handlers import TimedRotatingFileHandler

READ_INTERVAL_SECONDS = 10
READ_ONLY = False

logger = logging.getLogger(__name__)

def setup_logging():
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    trf_handler = TimedRotatingFileHandler("logs/the_foobar_home.log", when="h", interval=1, backupCount=5)        
    trf_handler.setFormatter(formatter)
    trf_handler.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)    

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(trf_handler)
    root_logger.addHandler(stream_handler)


def main(*args, **kwargs):
    try:
        asyncio.run(do_stuff_periodically())
    except (KeyboardInterrupt, SystemExit):
        handle_exit()

async def do_stuff_periodically():
    while True:
        await asyncio.gather(
            asyncio.sleep(10),
            plenticore.async_main(READ_ONLY)
        )

def handle_exit(*args):
    if db.connection_pool and db.connection_pool:
        db.connection_pool.closeall()
    logger.debug("Threaded PostgreSQL connection pool is closed")


if __name__ == "__main__":
    setup_logging()
    main()
