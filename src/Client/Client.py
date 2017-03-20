    # -*- coding: utf-8 -*-
import socket
from MessageReceiver import MessageReceiver
from MessageParser import MessageParser

class Client:
    """
    This is the chat client class
    """
    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """
        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # TODO: Finish init process with necessary code
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        self.handle_input()
        
    def disconnect(self):
        self.connection.disconnect()
        # TODO: Handle disconnection
        pass
    def receive_message(self, message):
        self.MessageReciever.run()
        pass
    def send_payload(self, data):
        # TODO: Handle sending of a payload
        pass
    def handle_input(self):
        while(True):
            userInput=raw_input("Awaiting user input\n")
            if(userInput[0:5]==('login')):
                loginString="login("+userInput[6:]+")"
                send_payload(loginString)
            elif(userInput[0:6]==("logout")):
                send_payload("logout")
    # More methods may be needed!


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations are necessary
    """
    client = Client('localhost', 9998)
