import asyncio
import logging

from peewee_async import PostgresqlDatabase
from peewee_async import Manager

io_loop = asyncio.get_event_loop()
psql_db = PostgresqlDatabase(database='betbot', user='betbot_user', password='devpass', host='127.0.0.1')
database_manager = Manager(psql_db, loop=io_loop)
database_manager.database.allow_sync = logging.ERROR
