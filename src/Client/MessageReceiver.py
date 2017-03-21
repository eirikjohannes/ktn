# -*- coding: utf-8 -*-
from threading import Thread
from MessageParser import MessageParser

class MessageReceiver(Thread):
	def __init__(self, client, connection):
		super(MessageReceiver,self).__init__()
		self.daemon = True
		self.client=client
		self.connection=connection
		self.msgParser=MessageParser()
	def run(self):
		print("Running messagereciever")
		while True:
			incomingMessage=self.connection.recv(4096)
			if incomingMessage!="":
				parsedMessage=self.msgParser.parse(incomingMessage)
				if parsedMessage=="logout":
					self.stop()
				else:
					print(parsedMessage)
				#self.stop()
		pass
	def stop(self):
		self.client.disconnect()
