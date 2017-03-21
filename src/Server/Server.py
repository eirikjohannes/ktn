# -*- coding: utf-8 -*-
import SocketServer
import json
import datetime
import time
import re
import atexit

"""
Variables and functions that must be used by all the ClientHandler objects
must be written here (e.g. a dictionary for connected clients)
"""
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

connections=[]
users=[]
history=[]

def addUser(user):
    global users
    users.append(user)
def closeConnection(username,connection):
    global connections
    global users
    if(username in users):
        users.remove(username)
        print("Removed username: "+ username)
    if(connection in connections):
        connections.remove(connection)
        print("Removed connection: ",connection)
    print bcolors.WARNING+("closeConnection ran")+bcolors.ENDC
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
        atexit.register(closeConnection(self.username,self))
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
                    self.data=jsonStr["content"]
                    self.request=jsonStr["request"]
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
            #"Switch case on request"
            if self.request=="login" and self.clientLoggedIn==False:
                print("login of user "+(self.data))
                global history
                global users
                if self.data in users:
                    response={"timestamp":timestamp,"sender":"Server","response":"error","content":"Username in use, choose another one."}
                    try:
                        payload=json.dumps(response)
                        self.connection.send(payload)
                    except:
                        print bcolors.FAIL + "Failed something"+bcolors.ENDC

                elif not(self.checkUsernameForCharacters(self.data)):
                    response={"timestamp":timestamp,"sender":"Server","response":"error","content":"Illegal characters, choose another username"}
                    try:
                        self.connection.send(json.dumps(response))
                    except:
                        print bcolors.FAIL + "Failed something"+bcolors.ENDC                    
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
                            response={
                                "timestamp":oldTimestamp,
                                "sender":oldSender,
                                "response":"history",
                                "content":oldContent
                                }
                            self.connection.send(json.dumps(response))
                            time.sleep(0.1)
                    self.clientLoggedIn=True
                    currTime=time.time()
                    timestamp=datetime.datetime.fromtimestamp(currTime).strftime('%H:%M:%S')
                    response={"timestamp":timestamp,"sender":"Server","response":"info","content":"Succesfully logged in as "+self.data
                    }
                    self.username=self.data
                    users.append(self.data)
                    self.clientLoggedIn=True
                    print self.username +" logged in sucessfully"
                    self.connection.send(json.dumps(response))
            #end "Login"
            elif self.request=="logout" and self.clientLoggedIn:
                print("Logout")
                for conn in connections:
                    conn.connection.send(json.dumps({"timestamp":timestamp,"response":"info","sender":"Server","content":self.username+" logged out"}))
                self.connection.send(json.dumps({"timestamp":timestamp,"response":"logout","sender":"Server"}))
                users.remove(self.username)
                connections.remove(self)
                self.clientLoggedIn=False
                self.username=""
                self.connection.close()
                break
            #end "logout"
            elif self.request=="names" and self.clientLoggedIn:
                print bcolors.WARNING+("Names")+bcolors.ENDC
                stringOfUsers="ListOfUsers:\n"
                for user in users:
                    stringOfUsers+= "-" +user+"\n"
                response={"timestamp":timestamp,"sender":"Server","response":"info","content":stringOfUsers}
                self.connection.send(json.dumps(response))
            #end "names"
            elif self.request=="msg" and self.clientLoggedIn:
                print("msg")
                global connections
                global history
                response={"timestamp":timestamp,"sender":self.username,"response":"message","content":self.data}
                payload=json.dumps(response)
                history.append(payload)
                for connection in connections:
                    connection.connection.send(payload)
            #end "msg"
            elif self.request=="help":
                print("help")
                content = "***HELP***\n" 
                content += "List of commands:\n"
                content += "-login to log onto the chat server\n-names for a list of all users\n-history for a list of all previous messages\n-logout to log off the server\n-help if you want to see this message again.\nGood luck"
                response = {"timestamp":timestamp,"sender":"Server","response":"info","content":content} 
                self.connection.send(json.dumps(response))
            #end "Help"
            elif self.request=="history":
                message="***Earlier chat history***"
                currTime=time.time()
                timestamp=datetime.datetime.fromtimestamp(currTime).strftime('%H:%M:%S')
                response={"timestamp":timestamp,"sender":"Server","response":"info","content":message}
                self.connection.send(json.dumps(response))  
                for earlierMessage in history:
                    jsonHis=json.loads(earlierMessage)
                    oldSender=jsonHis["sender"].encode()
                    oldTimestamp=jsonHis["timestamp"].encode()
                    oldContent=jsonHis["content"].encode()
                    response={
                        "timestamp":oldTimestamp,
                        "sender":oldSender,
                        "response":"history",
                        "content":oldContent
                        }
                    self.connection.send(json.dumps(response))
                    time.sleep(0.01)

            time.sleep(0.1)
            #end "History"
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


