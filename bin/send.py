import pika, os

from lib.db.models import User

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='producing', durable = True)

simple_result = {'scoreAway': '0',
                 'scoreHome': '1',
                 'teamHome': 'Orenburg',
                 'teamAway': 'Kazan',
                 'league': 'Russian Premier League',
                 'time': '17:00'}

bets = ('w1', 'w2', 'd')
bet_made_by_user = 'w1'

chat_list=[]

for user in User.select():
    chat_list.append(user.username)


win = 'Wow! Your bet wins! :)'
loose = 'Oh, I\'m sorry, your bet loose :('

def send_message_to_queue(number, status):
    channel.basic_publish(exchange = '',
                        routing_key = 'producing',
                        body = status+'\a'+chat_list[number],
                      properties = pika.BasicProperties(delivery_mode=2))

    print('[x] Message sent to {}'.format(chat_list[number]))



def delivery():
    i=0
    for ids in chat_list:
        if bet_made_by_user == bets[0] :
            send_message_to_queue(i,win)
        else:
            send_message_to_queue(i, loose)
    i+=1

connection.close()