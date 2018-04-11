import slackbot
import time
import os

def handle_command(slack_api, command, channel):
	
	EXAMPLE_COMMAND = 'do'
	if command.lower().startswith('hi') or command.lower().startswith('hey') or command.lower().startswith('hello'):
    		slack_api.rtm_send_message(channel, 'Hey, I\'m your slack bot, how may I help you?')
	else:
		slack_api.rtm_send_message(channel, 'Invalid Command: Not Understood')
	
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