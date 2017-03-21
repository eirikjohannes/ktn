# -*- coding: utf-8 -*-
from threading import Thread

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and it allows
    the chat client to both send and receive messages at the same time
    """

    def __init__(self, client, connection):
      """
      This method is executed when creating a new MessageReceiver object
      """

      # Flag to run thread as a deamon
      self.daemon = True
      self.client=client
      self.connection=connection

      # TODO: Finish initialization of MessageReceiver

    def run(self):
      while True:
      	try:
        	incomingMessage=connection.recieve()
      	except:
      		pass
      	if incommingMessage:
        	parsedMessage=MessageParser.parse(incomingMessage)
        	self.recieve_message(parsedMessage)
        else:

        	self.stop()
      # TODO: Make MessageReceiver receive and handle payloads

      pass

    def stop(self):
    	self.client.disconnect()
