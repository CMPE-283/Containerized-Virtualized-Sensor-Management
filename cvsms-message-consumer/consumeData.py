#!/usr/bin/python
# -*- coding: utf-8 -*-

import pika
import json,time,timeit
from cassandra.cluster import Cluster

# Cassandra
remainingTime = 30
try:
        cluster = Cluster(['127.0.0.1'])
        session = cluster.connect()
        session.execute('use sensorkeyspace')
except Exception as e:
        while remainingTime > 0:
                try:
                        start = timeit.default_timer()
                        cluster = Cluster(['127.0.0.1'])
                        session = cluster.connect()
                        if session is not None:
                                session.execute('use sensorkeyspace')
                                break
                except Exception as ex:
                        print ex
                        print 'Trying'
                        stop = timeit.default_timer()
                        remainingTime = remainingTime - (stop-start)
                        time.sleep(10)
                        continue

def on_message(channel, method_frame, header_frame, body):
    # print method_frame.delivery_tag
    data = json.loads(body)
    global session
    session.execute("""insert into sensordata (id,type,addedTimeStamp,date,epoch,unit,unit_symbol,value) 
    	values (%s,%s,dateof(now()),%s,%s,%s,%s,%s)""",
    	(data['sensor_id'],data['type'],data['date'],data['epoch'],data['unit'],data['unit_symbol'],data['value'])
    	)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

def main():
	try:
		# RabbitMQ
		credentials = pika.PlainCredentials('prasanna','likong123')
		parameters = pika.ConnectionParameters('localhost',5672,'/',credentials)
		connection = pika.BlockingConnection(parameters)
		channel = connection.channel()
		args = {"x-max-length": 7200}
		channel.queue_declare(queue = 'sensor_queue',arguments = args)
		channel.basic_consume(on_message, 'sensor_queue')
		print 'Started Consuming'
		channel.start_consuming()


	except KeyboardInterrupt:
		channel.stop_consuming()
	except Exception, e:
		raise e

if __name__=='__main__':
	main()
