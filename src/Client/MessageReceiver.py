# -*- coding: utf-8 -*-
from threading import Thread
from MessageParser import MessageParser
import atexit

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MessageReceiver(Thread):
	def __init__(self, client, connection):
		super(MessageReceiver,self).__init__()
		#self.thread = Thread(target=self.run)
		self.daemon = True
		self.client=client
		self.connection=connection
		self.msgParser=MessageParser()
	def run(self):
		while True:
			try:
				incomingMessage=self.connection.recv(4096)
			except:
				print bcolors.WARNING+"Failed when trying to read socket, restart program"+bcolors.ENDC
				break

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
