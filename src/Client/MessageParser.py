import json

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message':self.parse_message,
            'history':self.parse_history
	    # More key:values pairs are needed	
        }

    def parse(self, jsonPayload):
        try:
        	payload = json.loads(jsonPayLoad)# decode the JSON object
        except:
        	print("Error while loading json in messageparser\n"+payload)
        	return "error"
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
    	timestamp=payLoad["timestamp"]
    	errormsg=payLoad["content"]
    	return (timestamp+": Error recieved: "+errormsg)

    def parse_info(self, payload):
    	timestamp=payLoad["timestamp"]
    	infomsg=payLoad["content"]
    	return (timestamp+": Info: "+infomsg)

    def parse_history(self,payLoad):
    	timestamp=payLoad["timestamp"]
    	history=payLoad["content"]
    	return (timestamp+": History:\n"+history)
    def parse_message(self, payLoad):
    	timestamp=payLoad["timestamp"]
    	msg=payLoad["content"]
    	sender=payLoad["sender"]
    	return (timestamp+": "+sender+": "+content)

    # Include more methods for handling the different responses... 
