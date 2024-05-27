
from pathlib import Path
from dotenv import load_dotenv
import os
from flask import  request, Response
import slack 
# # from combinedbot import bot_client


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
speakCommandWhitelist = os.environ['SPEAK_COMMAND_WHITELIST']
bot_client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])



def speak():
    data = request.form
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')
    text = data.get('text')
    print (data)
    print(text)
    # bot_client.chat_postMessage(channel=channel_id, text=text)
    
    if user_id in speakCommandWhitelist:
        bot_client.chat_postMessage(channel=channel_id, text=text)
        return Response(), 200
    else: 
        return Response(), 200