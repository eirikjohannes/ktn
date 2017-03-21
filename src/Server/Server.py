# -*- coding: utf-8 -*-
import SocketServer
import json
import datetime
import time
import re

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""

connections=[]
users=[]
history=[]

def addUser(user):
    global users
    users.append(user)

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection=self.request

        print("Self:",self.client_address,"\n")
        self.username=""
        self.clientLoggedIn=False
        self.request=""
        self.data=""
        # Loop that listens for messages from the client
        connections.append(self)
        while True:
            global connections
            print("Connections:\n")
            for con in connections:
                print("\t",con,"\n")
            print("#"*30)
            
            recStr = self.connection.recv(4096)
            
            currTime=time.time()
            timestamp=datetime.datetime.fromtimestamp(currTime).strftime('%H:%M:%S')
            if recStr!="":
                #recStr=self.connection.recv(4096)
                try:
                    jsonStr=json.loads(recStr)
                    self.data=jsonStr["content"].encode()
                    self.request=jsonStr["request"].encode()
                except ValueError:
                    print("Not JSONObject, retry")
            elif recStr=="":
                self.request=""
                self.data=""
                #do nothing
            else:
                try:
                    jsonStr=json.loads(recStr)
                    self.data=jsonStr["content"]
                    self.request=jsonStr["request"]
                except:
                    print("Error while reading json object")

            if self.request=="login" and self.clientLoggedIn==False:
                print("login of user "+(self.data))
                global history
                global users
                if self.data in users:
                    response={"timestamp":timestamp,"sender":"Server","response":"error","content":"Username in use, choose another one."}
                elif not(self.checkUsernameForCharacters(self.data)):
                    response={"timestamp":timestamp,"sender":"Server","response":"error","content":"Illegal characters, choose another username"}
                else:
                    print("Sucess")
                    message="***Earlier chat history***"
                    response={"timestamp":timestamp,"sender":"Server","response":"info","content":message}
                    self.connection.send(json.dumps(response))
                    if len(history)>0:  
                        for earlierMessage in history:
                            jsonHis=json.loads(earlierMessage)
                            oldSender=jsonHis["sender"].encode()
                            oldTimestamp=jsonHis["timestamp"].encode()
                            oldContent=jsonHis["content"].encode()
                            response={"timestamp":oldTimestamp,"sender":oldSender,"response":"history","content":oldContent}
                            self.connection.send(json.dumps(response))
                            time.sleep(0.1)
                    self.clientLoggedIn=True
                    currTime=time.time()
                    timestamp=datetime.datetime.fromtimestamp(currTime).strftime('%H:%M:%S')
                    response={"timestamp":timestamp,"sender":"Server","response":"info","content":"Succesfully logged in as "+self.data}
                    self.username=self.data
                    users.append(self.data)
                    self.clientLoggedIn=True
                    print self.username +" logged in sucessfully"
                self.connection.send(json.dumps(response))
            elif self.request=="logout" and self.clientLoggedIn:
                print("Logout")
                self.connection.send(json.dumps({"response":"logout","sender":"Server"}))
                users.remove(self.username)
                connections.remove(self)
                self.clientLoggedIn=False
                self.username=""
                self.connection.close()
                break
            elif self.request=="names" and self.clientLoggedIn:
                print("Names")
                stringOfUsers=""
                for user in users:
                    stringOfUsers+= "-" +user+"\n"
                response={"timestamp":timestamp,"sender":"Server","response":"info","content":stringOfUsers}
                self.connection.send(json.dumps(response))

            elif self.request=="msg" and self.clientLoggedIn:
                print("msg")
                global connections
                global history
                response={"timestamp":timestamp,"sender":self.username,"response":"message","content":self.data}
                payload=json.dumps(response)
                history.append(payload)
                for connection in connections:
                    connection.connection.send(payload)

            elif self.request=="help":
                print("help")
                content = "***HELP***\n" 
                content += "List of commands:\n"
                content += "-login <username> to log onto the chat server\n-names for a list of all users\n-history for a list of all previous messages\n-logout to log off the server\n-help if you want to see this message again.\nGood luck"
                response = {"timestamp":timestamp,"sender":"Server","response":"info","content":content} 
                self.connection.send(json.dumps(response))

                #self.connection.send(json.dumps({"timestamp":timestamp,"sender":"Server","response":"error","content":"No access"}))
            # TODO: Add handling of received payload from client
    def checkUsernameForCharacters(self,username):
        return bool(re.match('[a-zA-Z0-9]',username))

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations are necessary
    """
    HOST, PORT = 'localhost', 9998
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()


