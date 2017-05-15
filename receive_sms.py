from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import googlemaps
from datetime import datetime 
import re
import json

app = Flask(__name__)

# get api key json
with open('auth.json') as credentials:
	data = json.load(credentials)
google_api_key = data["googlemaps"]["key"]
gmaps = googlemaps.Client(key=google_api_key)

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
	# user texts have to come in the form 
	# from: 1234 Main Street - to: 2345 Main Ave - mode: driving

	# parse user input
	user_body = request.form.get('Body').split('-')
	user_from_address = user_body[0][5:-1]
	user_to_address = user_body[1][4:]	
	user_mode_transport = ''

	# check if user specified mode
	try:
		user_mode_transport = user_body[2][7:]
		user_mode_transport.replace(" ", "")
	except IndexError:
		pass

	# get google maps directions
	now = datetime.now()
	try:
		directions_result = gmaps.directions(user_from_address, user_to_address,mode=user_mode_transport.replace(" ", ""), departure_time=now)
	except googlemaps.exceptions.ApiError:
		resp = MessagingResponse()
		resp.message("No directions found. Are you sure you formatted the request correctly?")
		return str(resp)

	# get the leg/steps of the route
	driving_steps = directions_result[0]['legs'][0]['steps']
	if(len(driving_steps) > 25):
		resp = MessagingResponse()
		resp.message('The directions you requested exceeds text limits, we are unable to serve this. ')
		return str(resp)

	response_body = ''
	step_counter = 1

	# iterate through each leg/step of the route
	for i in range(len(driving_steps)):
		distance = driving_steps[i]['distance']['text']
		instruction = driving_steps[i]['html_instructions']
		instruction = re.sub('<[^<]+?>', '', instruction)

		# figure out how to phrase the instruction gramatically (very rough parsing)
		grammar = instruction.split(' ')[0]

		if grammar == 'Turn' or grammar == 'Merge' or grammar == 'Take' or grammar == 'Slight':
			current_instruction = str(step_counter) + ': ' + instruction + ' in ' + distance + '.'
		elif grammar == 'Head' or grammar == 'Continue' or grammar == 'Keep':
			current_instruction = str(step_counter) + ': ' + instruction + ' for ' + distance + '.'
		else:
			current_instruction = str(step_counter) + ': ' + instruction + '. Distance: ' + distance + '.'

		response_body += current_instruction + '\n'
		step_counter += 1

	resp = MessagingResponse()
	resp.message(response_body)
	return str(resp)

if __name__ == '__main__':
	app.run(debug=True)
