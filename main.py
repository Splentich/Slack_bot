import slackbot
import time	
import os
import requests
import json

CONVERT_TO_CELSIUS = 273.15

""" This method handles bot's logic and replies to users """
def handle_command(slack_api, command, channel):
    	
		if command.lower().startswith('hi') or command.lower().startswith('hey') or command.lower().startswith('hello'):
    			slack_api.rtm_send_message(channel, 'Hi, I\'m your weather bot. If you would you like to see the current weather in Vancouver type "weather" ')
		elif command.lower().startswith('weather'):
    			data = get_weather()
    			for i in data:
    					slack_api.rtm_send_message(channel, ("%s: %s" % (i, data[i])))
		else:
				slack_api.rtm_send_message(channel, 'Sorry, I don\'t understand this')			
				

""" API call for OpenWeather. This is a dicrect call for the weather in Vancouver. Weather data is being reached by city ID. """     				
def get_weather():
	response = requests.get('http://api.openweathermap.org/data/2.5/weather?id=6173331&appid=7d82f7ba43beaf7ee5c79bca20718fba').json()
	weather = {
  			'Temperature': u'%d \u2103' % (response['main']['temp'] -  CONVERT_TO_CELSIUS),
 	 		'Humidity': '%s %%' % response['main']['humidity'],
  			'Wind': '%s m/s' % response['wind']['speed'],
  			'Precipitation': response['weather'][0]['main'],
	}
	return weather
	
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