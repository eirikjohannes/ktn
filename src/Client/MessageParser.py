

class MessageParser():
    def __init__(self):

        self.possible_responses = {
            'error': self.parse_error,
            'info': self.parse_info,
            'message':self.parse_message,
            'history':self.parse_history
	    # More key:values pairs are needed	
        }

    def parse(self, payload):
        payload = json.loads(payLoad)# decode the JSON object

        if payload['response'] in self.possible_responses:
            if payload['response']=='error'{
                return parse_error(payload)
            }
            else if payload['response']=='info'{
                return parse_info(payload)
            }
            return self.possible_responses[payload['response']](payload)
        else:
            return "Invalid message recieved"
            # Response not valid

    def parse_error(self, payload):
    
    def parse_info(self, payload):


    def parse_history(self,payLoad):

    def parse_message(self, payLoad):
    
    # Include more methods for handling the different responses... 
