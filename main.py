import db
import plenticore
import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from logging.handlers import TimedRotatingFileHandler

READ_INTERVAL_SECONDS = 10
READ_ONLY = False

logger = logging.getLogger(__name__)

def setup_logging():
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    handler = TimedRotatingFileHandler("logs/foobar_home.log", when="h", interval=1, backupCount=5)        
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    ch.setLevel(logging.INFO)    

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(handler)
    root_logger.addHandler(ch)


def main2():
    setup_logging()
    logger.info("test info")
    logger.error("test error")
    db.test_log()
    logger.warning("test warn")
    logger.debug("test debug")


def main(*args, **kwargs):
    setup_logging()
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
    main()
