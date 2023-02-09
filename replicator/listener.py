import logging
import os
import asyncio
import psycopg2
from dotenv import load_dotenv

from logger import setup_logger
from sql_operations import operations
from utils import get_notify_data


setup_logger()
logger = logging.getLogger("replicator")

load_dotenv()


HOST1 = os.getenv('HOST1')
DBNAME1 = os.getenv('DBNAME1')
HOST2 = os.getenv('HOST2')
DBNAME2 = os.getenv('DBNAME2')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')

connection_1 = psycopg2.connect(
    host=HOST1,
    dbname=DBNAME1,
    user=USER,
    password=PASSWORD)
connection_1.set_isolation_level(
    psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cursor_1 = connection_1.cursor()
cursor_1.execute("LISTEN users_changes1;")


connection_2 = psycopg2.connect(
    host=HOST2,
    dbname=DBNAME2,
    user=USER,
    password=PASSWORD)
connection_2.set_isolation_level(
    psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)

cursor_2 = connection_2.cursor()
cursor_2.execute("LISTEN users_changes2;")


def handle_notify(connection, cursor):
    connection.poll()
    for notify in connection.notifies:
        logger.info(notify.payload)
        operation, data = get_notify_data(notify.payload)
        try:
            operations.get(operation)(cursor, data, 'users')
        except Exception as e:
            logger.info(e)
    connection.notifies.clear()


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.add_reader(connection_1, handle_notify, connection_1, cursor_2)
loop.add_reader(connection_2, handle_notify, connection_2, cursor_1)
loop.run_forever()
