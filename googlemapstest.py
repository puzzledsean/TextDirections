# just a sandbox trying to figure out google maps direction API

import googlemaps
from datetime import datetime 
import re
import json

with open('auth.json') as credentials:
	data = json.load(credentials)

google_api = data["googlemaps"]["key"]

gmaps = googlemaps.Client(key=google_api)

now = datetime.now()
directions_result = gmaps.directions("Boston University", "New York University", departure_time=now)

driving_steps = directions_result[0]['legs'][0]['steps']

response_body = ''

step_counter = 1
for i in range(len(driving_steps)):
	distance = driving_steps[i]['distance']['text']
	instruction = driving_steps[i]['html_instructions']
	instruction = re.sub('<[^<]+?>', '', instruction)

	# figure out how to phrase the instruction gramatically (very rough implementation)
	grammar = instruction.split(' ')[0]

	if grammar == 'Turn' or grammar == 'Merge' or grammar == 'Take' or grammar == 'Slight':
		current_instruction = str(step_counter) + ': ' + instruction + ' in ' + distance + '.'
	elif grammar == 'Head' or grammar == 'Continue' or grammar == 'Keep':
		current_instruction = str(step_counter) + ': ' + instruction + ' for ' + distance + '.'
	else:
		current_instruction = str(step_counter) + ': ' + instruction + '. Distance: ' + distance + '.'

	response_body += current_instruction + '\n'
	step_counter += 1

print(response_body)
