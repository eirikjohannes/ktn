# -*- coding: utf-8 -*-
import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message':self.parse_message,
            'history':self.parse_history,
            'logout':self.parse_logout
	    # More key:values pairs are needed	
        }

    def parse(self, jsonPayload):
				#payload={"content":"None"}
				payload = json.loads(jsonPayload)
				if payload['response'] in self.possible_responses:
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
    	return (timestamp+": Error recieved: "+errormsg)

    def parse_info(self, payload):
    	timestamp=payload["timestamp"]
    	infomsg=payload["content"]
    	return (timestamp+": Info: "+infomsg)

    def parse_history(self,payload):
    	timestamp=payload["timestamp"]
    	history=payload["content"]
    	return (timestamp+": History:\n"+history)
    def parse_message(self, payload):
    	timestamp=payload["timestamp"]
    	msg=payload["content"]
    	sender=payload["sender"]
    	return (timestamp+": "+sender+": "+msg)

    def parse_logout(self,payLoad):
    	return "logout"
    # Include more methods for handling the different responses... 
