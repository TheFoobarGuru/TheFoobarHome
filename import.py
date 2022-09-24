import db
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from logging.handlers import TimedRotatingFileHandler
import pytz




@db.with_cursor(write=True)
def save(*args, **kwargs) -> None:

    cursor = kwargs.get("cursor")
    data = []
    with open('/Users/denis/Documents/import_log/import.csv') as file:
        lines = file.readlines()
        for line in lines:
            values = line.split(";")
            data.append(
                (datetime.fromtimestamp(int(values[0].strip())), float(values[1].strip()), float(values[2].strip()), float(values[3].strip()), float(values[4].strip()), 0, 0)
            )        
    
    args = ','.join(cursor.mogrify("(%s, %s, %s, %s, %s, %s, %s)", i).decode('utf-8')
                for i in data)


    SQL = "INSERT INTO home_consumption2 (time, from_battery, from_pv, from_grid, total, home_p, home_own_p) VALUES " + args
    cursor.execute(SQL)


@db.with_cursor(write=True)
def read(*args, **kwargs):
    cursor = kwargs.get("cursor")
    cursor.execute("SELECT * FROM home_consumption2 hc2;")
    # cursor.execute("SELECT * FROM home_consumption2 hc2 WHERE hc2.time = '2022-09-18 02:00:01';")
    # cursor.execute("DELETE FROM home_consumption2 hc2 WHERE hc2.time = '2022-09-18 02:00:01';")
    # cursor.execute("DELETE FROM home_consumption hc WHERE hc.time IN (SELECT hc2.time from home_consumption hc2);")
    # cursor.execute("SELECT * FROM home_consumption2 ORDER BY time DESC limit 1")
    home_consumptions = []
    for row in cursor.fetchall():
        print(row.time)


read()

# save()