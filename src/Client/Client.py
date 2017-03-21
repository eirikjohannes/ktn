    # -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

import json
class Client:
  """
  This is the chat client class
  """
  def __init__(self, host, server_port):
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host=host
		self.server_port=server_port
		self.run()
  def run(self):
    # Initiate the connection to the server
		self.connection.connect((self.host, self.server_port))
		self.msgRecTask=MessageReciever.init(self.client,self.connection)
		self.msgRecTask.run()
		self.userName="notAUser"
		self.loggedOn=True 
		print("Welcome to this chat client - type \"-login <username>\" to log on") 		
		self.handle_input()
  def disconnect(self):
		self.connection.disconnect()
		pass
  def receive_message(self, message):
		print(message)
		pass
  def send_payload(self, data):
		self.connection.send(data)
    # TODO: Handle sending of a payload
		pass
  def handle_input(self):
		empty=""
		while True:
			userInput=raw_input("_")
			if userInput[0:6]=="-login":
				userName=userInput[7:]
				data={"request":"login","content":userName}
				try:
					payload=json.dumps(data)
					self.send_payload(payload)
					self.loggedOn=True
				except :
					print("Error while logging on")
					continue

			elif userInput[0:7]=="-logout" and loggedOn:
				payload=json.dumps({"request":"logout","content":userName})
				self.send_payload(payload)
				self.loggedOn=False
				self.disconnect()
				print("Succesfully logged out\n")

			elif userInput[0:5]=="-help":
				payload=json.dumps({"request":"help","content":userInput[6:]})
				self.sendpayload(payload)

			elif userInput=="-history" and self.loggedOn:
				payload=json.dumps({"request":"history","content":empty})
				self.send_payload(payload)

			elif userInput=="-names" and self.loggedOn:
				payload=json.dumps({"request":"names","content":empty})

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

    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
