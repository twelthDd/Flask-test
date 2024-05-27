import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter

env_path = Path('.') / '.env'
load_dotenv (dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],"/slack/events",app)
client = slack.WebClient(token=os.environ["SLACK_BOT_TOKEN"])
bot_client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
BOT_ID = bot_client.api_call("auth.test")['user_id']
print (BOT_ID)

#* To post a message via the bot
client.chat_postMessage(channel='U0607C9UUE6', text="BRING IT!")

@slack_event_adapter.on("message")
def message(payload):
    # print(payload)
    # event = payload.get(event, {})
    # channel_id = event.get('channel')
    # user_id = event.get('user')
    # text = event.get('text')
    # client.chat_postMessage(channel=channel_id, text=text)
    # print (event)
    print(payload)

# if __name__ == "__main__":
    # app.run(debug=True, port="8000")