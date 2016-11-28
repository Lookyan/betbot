import logging

from aiotg.bot import logger as aiotg_logger

from lib.commands import bot

logger = logging.getLogger(__name__)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    aiotg_logger.setLevel(logging.INFO)
    logger.info('Starting bot')
    bot.run()
