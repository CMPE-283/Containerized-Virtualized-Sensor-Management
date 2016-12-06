#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template

import time,timeit
from datetime import timedelta as td
from datetime import datetime as dt
from random import uniform
import uuid
import json
from flask_cors import CORS, cross_origin
from cassandra.cluster import Cluster



app = Flask(__name__)
CORS(app)

START_DATE = "01-Apr-12"

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


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getClosingData")
def getClosingData():
	data = dict()
	global START_DATE
	data['date'] = START_DATE
	data['close'] = round(uniform(1,100),2)
	START_DATE = (dt.strptime(START_DATE,"%d-%b-%y") + td(days=1)).strftime("%d-%b-%y")
	return json.dumps(data, sort_keys=False,indent=4, separators=(',', ': '))


@app.route("/getData/<sensor_id>")
def getdata(sensor_id):
	global session
	result = session.execute("select id, type, date, value, unit, unit_symbol from sensordata where id='%s' order by addedTimeStamp desc limit 1" % (sensor_id))
	data = dict()
	for row in result:
		data['date'] = row.date
		data['value'] = row.value
		break
	# epoch = time.time()
	# data = dict()
	# data['type'] = sensortype
	# data['sensor_id'] = sensor_id
	# data['epoch'] = epoch
	# if sensortype == 'temperature':
	# 	value = round(uniform(40,90),2)
	# 	data['unit_symbol'] = '°F'
	# 	data['unit'] = 'Degree Fahrenheit'
	# elif sensortype == 'humidity':
	# 	value = round(uniform(0,100),2)
	# 	data['unit_symbol'] = '%'
	# 	data['unit'] = 'Percent'
	# else:
	# 	value = round(uniform(-1,1),2)
	# 	data['unit_symbol'] = ''
	# 	data['unit'] = 'unit'
	# data['value'] = value
	return json.dumps(data, sort_keys=False,indent=4, separators=(',', ': '))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
