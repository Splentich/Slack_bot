from slackclient import SlackClient
import os


""" Connecting to Slack API """
def connect():
    
	slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
	return slack_client

""" Parsing response from Slack API """
def parseResponse(response, botID):
    	
	bot_at_id = '<@'+botID+'>'
	if response and len(response):
		for k in response:
			if k and 'text' in k:
				if bot_at_id in k['text']:
					return k['text'].split(bot_at_id)[1].strip(), k['channel']
	return None, None 

""" Getting BOT ID from Slack API """
def getBotId(bot_name):
    	
	slack_client = connect()
	api_call = slack_client.api_call('users.list')
	users = api_call['members']
	if api_call.get('ok'):
		for user in users:
    			if 'name' in user and bot_name in user.get('name') and not user.get('deleted'):
    					return user.get('id')
			




