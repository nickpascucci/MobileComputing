#! /usr/bin/python

import socket
import random
import time
import struct


MAX_NODES = 100
NUM_READINGS = 10


def start_server():
	print "Starting faux sensor network..."

	HOST = ''                 
	PORT = 9002
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((HOST, PORT))
	s.listen(1)
	conn, addr = s.accept()
	print 'Connected by', addr
	conn.send('U ')
	data = conn.recv(1024)
	print "Protcol: ", data

	while True:
    		time.sleep(random.random())
		conn.send(get_random_fake_data())

	conn.close()


def get_random_fake_data():

	ids = range(1, MAX_NODES)

	base_sensor_reading = random.randint(15000, 31000)
	readings = []
	for i in range(NUM_READINGS):
		readings.append(random.randint(0, 500) + base_sensor_reading)

	source_id = random.choice(ids)

	result = struct.pack("!ibiibbbHHHHHHHHHH", 0, source_id, 0, 0, 0, 0, 0, readings[0], readings[1], readings[2], readings[3], readings[4], readings[5], readings[6], readings[7], readings[8], readings[9])

	print "SIZE: ", struct.calcsize("!ibiibbbHHHHHHHHHH")

	return result


start_server()
