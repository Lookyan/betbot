import asyncio

import pika
from aiotg import Bot

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='producing', durable=True)

print(' [*] Waiting for messages. To exit press CTRL+C')

async def send_results(chat_id, message):
    bot = Bot(api_token=os.environ['API_KEY'])
    await bot.send_message(chat_id, message)

def callback(ch, method, properties, body):
    tmp_message=body.decode()
    tmp_message, chat_id = tmp_message.split('\a')
    chat_id=int(chat_id)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_results(chat_id,tmp_message))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)

channel.basic_consume(callback,
                      queue='producing')

channel.start_consuming()
