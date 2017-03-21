    # -*- coding: utf-8 -*-
import socket
import json
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser
from threading import Thread

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Client:
  def __init__(self, host, server_port):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host=host
		self.server_port=server_port
		self.msgRecTask=MessageReceiver(self,self.connection)
		self.run()
  def run(self):
    # Initiate the connection to the server
		self.connection.connect((self.host, self.server_port))
		self.msgRecTask.start()
		self.userName="notAUser"
		self.loggedOn=False 
		print bcolors.OKBLUE+("Welcome to this chat client - type \"-login\" to log on")+bcolors.ENDC 		
		while True:
			userInput=raw_input(":")
			if userInput=="-login":
				userName=raw_input("Username: ")
				data={"request":"login","content":userName.encode()}
				print(userName)
				try:
					payload=json.dumps(data)
					self.send_payload(payload)
					self.loggedOn=True
				except :
					print("Error while logging on")
					#self.msgRecTask.stop()
					#self.msgRecTask.start()

			elif userInput=="-logout" and self.loggedOn:
				print("Got here")
				payload=json.dumps({"request":"logout","content":self.userName})
				self.send_payload(payload)
				self.loggedOn=False
				self.disconnect()
				print("Succesfully logged out\n")

			elif userInput=="-help":
				payload=json.dumps({"request":"help","content":""})
				self.send_payload(payload)

			elif userInput=="-history" and self.loggedOn:
				payload=json.dumps({"request":"history","content":""})
				self.send_payload(payload)

			elif userInput=="-names" and self.loggedOn:
				payload=json.dumps({"request":"names","content":""})
				self.send_payload(payload)
			else:
				if self.loggedOn:
					data={"request":"msg","content":userInput}
					try:
						payload=json.dumps(data)
						self.send_payload(payload)
					except:
						print("Error while sending msg")
						continue
				else:
					print("Invalid operation, consider logging in")
		pass
  def disconnect(self):
		self.connection.close()
		pass
  def receive_message(self, message):
		print(message)
		pass
  def send_payload(self, data):
		self.connection.send(data)
		pass
    # More methods may be needed!


if __name__ == '__main__':
	client = Client('localhost', 9998)
