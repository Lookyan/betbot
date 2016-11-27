import asyncio
import os

import pika
from aiotg import Bot

bot = Bot(api_token=os.environ['API_KEY'])

loop = asyncio.get_event_loop()

async def send_results(chat_id, message):
    await bot.send_message(chat_id, message)


def callback(ch, method, properties, body):
    tmp_message = body.decode()
    tmp_message, chat_id = tmp_message.split('\a')
    chat_id = int(chat_id)
    loop.run_until_complete(send_results(chat_id, tmp_message))
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='localhost'
        )
    )
    channel = connection.channel()

    channel.queue_declare(queue='push', durable=True)

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        callback,
        queue='push'
    )

    channel.start_consuming()

if __name__ == '__main__':
    main()
