#-*- coding: utf-8 -*-

import sys
import time
from datetime import datetime
from random import uniform
import uuid
import json
import pika
import os

def generateSensorDataOf(sensortype,channel,frequency=1):
	SENSOR_ID = os.environ['sensorid']
	try:
		while True:
			epoch = time.time()
			data = dict()
			data['type'] = sensortype
			data['sensor_id'] = SENSOR_ID
			data['epoch'] = epoch
			data['date'] = datetime.now().strftime("%d-%b-%y %H:%M:%S")
			if sensortype == 'temperature':
				value = round(uniform(40,90),2)
				data['unit_symbol'] = '°F'
				data['unit'] = 'Degree Fahrenheit'
			elif sensortype == 'humidity':
				value = round(uniform(0,100),2)
				data['unit_symbol'] = '%'
				data['unit'] = 'Percent'
			else:
				value = round(uniform(5,15),2)
				data['unit_symbol'] = ''
				data['unit'] = 'unit'
			data['value'] = value
			# print json.dumps(data, sort_keys=False,indent=4, separators=(',', ': '))
			channel.basic_publish(exchange='',routing_key='sensor_queue',body=json.dumps(data))
			time.sleep(3)
	except Exception, e:
		print 'error'
		raise e


def main():
	try:
		sensortype = os.environ['sensortype']

		# Connection to Rabbitmq
		credentials = pika.PlainCredentials('********','******')
		parameters = pika.ConnectionParameters('**.**.***.***',****,'/',credentials)
		connection = pika.BlockingConnection(parameters)
		
		# Channel
		channel = connection.channel()
		
		#set max queue size
		args = {"x-max-length": 7200}

		# Declare queue
		channel.queue_declare(queue='sensor_queue', arguments=args)
		
		# Start Generating Sensor Data
		generateSensorDataOf(sensortype,channel)

		connection.close()
	except KeyboardInterrupt:
		print '\nstopping sensor'
		connection.close()
	except Exception, e:
		raise e



if __name__=='__main__':
	main()
