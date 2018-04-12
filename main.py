import slackbot
import time	
import os
import requests
import json


def handle_command(slack_api, command, channel):
    	
		if command.lower().startswith('hi') or command.lower().startswith('hey') or command.lower().startswith('hello'):
    			slack_api.rtm_send_message(channel, 'Hi, I\'m your weather bot. Would you like to see the current weather in Vancouver? Type "weather" ')
		elif command.lower().startswith('weather'):
    			weather_conditions = get_weather()
    			for i in weather_conditions:
    					slack_api.rtm_send_message(channel, '\n'+str(i)+' : '+str(weather_conditions[i]))
		else:
				slack_api.rtm_send_message(channel, 'Sorry, I don\'t understand this')			
				
    				
def get_weather():
	response = requests.get('http://api.openweathermap.org/data/2.5/weather?id=6173331&appid=7d82f7ba43beaf7ee5c79bca20718fba')	
	json_object = response.json()
	temp = float(json_object['main']['temp'])
	temp_celius = int(temp - 273.15)
	humidity = int(json_object['main']['humidity'])
	wind_speed = float(json_object['wind']['speed'])
	weather = json_object['weather'][0]['main']
	weather_dictionary = dict({'temperature': temp_celius, 'humidity': humidity, 'wind': wind_speed, 'precipitation': weather})
	return weather_dictionary
	
def main():
    	
	READ_WEBSOCKET_DELAY = 1 
	slack_api = slackbot.connect()
	botname = os.environ.get("BOTNAME")
	BOT_ID = slackbot.getBotId(botname)

	if slack_api.rtm_connect():
		print 'SLACK_BOT is running'
		while True:
			command, channel = slackbot.parseResponse(slack_api.rtm_read(), BOT_ID)
			if command and channel:
				handle_command(slack_api, command, channel)
			time.sleep(READ_WEBSOCKET_DELAY)
	else:
		print 'Connection failed' 

if __name__ == '__main__':
	main()