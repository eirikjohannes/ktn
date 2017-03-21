# -*- coding: utf-8 -*-
import json
import os
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            "error": self.parse_error,
            "info": self.parse_info,
            "message":self.parse_message,
            "history":self.parse_history,
            "logout":self.parse_logout
	    # More key:values pairs are needed	
        }

    def parse(self, jsonPayload):
        payload={"content":"None"}
        try:
            payload = json.loads(jsonPayload)
        except:
            print("Error while loading jsonPayload")
            pass
        if payload["response"] in self.possible_responses:
    #if payload['response']=='error':
    #  return parse_error(payload)
    #elif payload['response']=='info':
    #  return parse_info(payload)
    #elif payload['response']=='history':
   	# return parse_history(payload)
    #elif payload['response']=='msg':
    #	return parse_message(payload)
    #else:
            return self.possible_responses[payload['response']](payload)
        else:
            return ("Recieved message not in possible responses, recieved type:"+payload['response'])
    # Response not valid

    def parse_error(self, payload):
    	timestamp=payload["timestamp"]
    	errormsg=payload["content"]
    	return bcolors.FAIL+(timestamp+": Error recieved: "+errormsg)+bcolors.ENDC

    def parse_info(self, payload):
    	timestamp=payload["timestamp"]
    	infomsg=payload["content"]
    	return (timestamp+": Info: "+infomsg)

    def parse_history(self,payload):
    	timestamp=payload["timestamp"]
    	history=payload["content"]
        sender=payload["sender"]
        if sender=="Server":
            return bcolors.HEADER+("\n\n\n"+timestamp+": History:\n"+history)+bcolors.ENDC
        else:
            return (timestamp+": "+sender+" said:\t"+history)
            
    def parse_message(self, payload):
    	timestamp=payload["timestamp"]
    	msg=payload["content"]
    	sender=payload["sender"]
    	return bcolors.OKGREEN+(timestamp+": "+sender+": "+msg)+bcolors.ENDC

    def parse_logout(self,payLoad):
    	return "logout"
    # Include more methods for handling the different responses... 
