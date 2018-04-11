from slackclient import SlackClient
import os
import time

def connect():
    
	slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
	return slack_client

def parseResponse(response, botID):
	bot_at_id = '<@'+botID+'>'
	if response and len(response):
		for obj in response:
			if obj and 'text' in obj:
				if bot_at_id in obj['text']:
					return obj['text'].split(bot_at_id)[1].strip(), obj['channel']
	return None, None 

def getBotId(bot_name):
    
	slack_client = connect()
	api_call = slack_client.api_call('users.list')
	users = api_call['members']
	if api_call.get('ok'):
		for user in users:
    			if 'name' in user and bot_name in user.get('name') and not user.get('deleted'):
    					return user.get('id')
			




