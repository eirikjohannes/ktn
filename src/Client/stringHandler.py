
import time 
import json

def main():
	while(1):
		userInput=raw_input("Awaiting user input\n")

		jsonInput=json.dumps({"request".encode():userInput})

		if(userInput[0:5]==('login')):
			loginString="login("+userInput[6:]+")"
			print(loginString)
			output=json.loads(jsonInput)
			print("After json conversion: "+output["request"])#send_payload(loginString)
		elif(userInput[0:6]==("logout")):
			print("logout")
		else:
			for i in range(0,len(userInput)):
				print(userInput[i])
			print("invalid,"+userInput[0:])
			#send_payload("logout")
		print("Time is: ",time.time())
main()