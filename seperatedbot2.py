import slack 
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask, request, Response
from slackeventsapi import SlackEventAdapter
import string
import json
from speakcommand import speak
from welcomemessage import WelcomeMessage

#* loads the .env file
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

#* creates flask app and the slack event adapter (used to receive data from slack api), slack client (used to comunicate with slack api) and defines BOT_ID
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ["SIGNING_SECRET"], "/slack/events", app)
client = slack.WebClient(token=os.environ['SLACK_USER_TOKEN'])
bot_client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
BOT_ID = bot_client.api_call("auth.test")['user_id']


whitelisted_users =  ["U06031QSBSB", "U0607TBATL3", "U04KMTN3JC8", "U04KHFCTMUH", "U04JYH0TXQS", "U060FS0PXGU", "U04KN83QUN4", "U04KB68EULR", "U0603URJGDT", "U04JRURDZSA", "U060L9L613Q", "U060KGX8RA5", "U0600QD62EA", BOT_ID, None]
# speakCommandWhitelist = os.environ['SPEAK_COMMAND_WHITELIST']

#* defines a list for the welcome message and message count variables (Noah)
WelcomeMessages = {}
message_counts = {}

#* (Nour)
messages_set = set()
ts_to_delete = set()

#! test bad words list (Noah)
BAD_WORDS = []

#* sends the welcome message class to user (Noah)
def send_welcome_message(channel, user):

    if channel not in WelcomeMessages:
        WelcomeMessages[channel] = {}

    if user in WelcomeMessages[channel]:
        return

    welcome = WelcomeMessage(channel, user)
    message = welcome.get_message()
    response = bot_client.chat_postMessage(**message)
    welcome.timestamp = response['ts']
    
    WelcomeMessages[channel][user] = welcome

#* checks messages to see if they contain words from the "BAD_WORDS" list (also removes punctuation from message)
def check_if_bad_words(message):
    msg = message.lower()
    msg = msg.translate(str.maketrans('', '', string.punctuation))
    
    return any(word in msg for word in BAD_WORDS)


@slack_event_adapter.on('message')
def message(payload):
    # print(payload)
    event = payload.get("event", {})
    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    print (text)
    timestamp = event.get("ts")
    event_type = event.get("type")
    #* Noah's part of the bot (the bot is still being combined)
    if user_id != None and BOT_ID != user_id:
        if user_id in message_counts:
            message_counts[user_id] += 1
        else:
            message_counts[user_id] = 1
        
        if text.lower() == 'welcome_message.test':
            send_welcome_message(f'@{user_id}', user_id)
            
        elif check_if_bad_words(text):
            ts = event.get('ts')
            bot_client.chat_postMessage(
                channel=channel_id, thread_ts=ts, text = "That is a bad word!(TESTING)")
    #* Nours's part of the bot (the bot is still being combined)
    
    if len(text) == 1:
        client.chat_delete(channel=channel_id, ts=timestamp)
    elif not user_id in whitelisted_users and channel_id == "C04KARSQMAM":
        messages_set.add(timestamp)
        for ts in messages_set:
            
            ts_to_delete.add(ts)
            try:
                client.chat_delete(channel=channel_id, ts=ts)
            except Exception as e:
                #//print(e)
                pass
        try:
            while len(messages_set) != 0:
                messages_set.difference_update(ts_to_delete)
            
            ts_to_delete.discard(ts_to_delete[0])
        except:
            pass

@slack_event_adapter.on('member_joined_channel')
def welcome_new_user(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')

    if user_id != BOT_ID:
        send_welcome_message(f'@{user_id}', user_id)
        
@ slack_event_adapter.on('reaction_added')
def reaction(payload):
    event = payload.get('event', {})
    channel_id = event.get('item', {}).get('channel')
    user_id = event.get('user')

    if f'@{user_id}' not in WelcomeMessages:
        return

    welcome = WelcomeMessages[f'@{user_id}'][user_id]
    welcome.completed = True
    welcome.channel = channel_id
    message = welcome.get_message()
    updated_message = bot_client.chat_update(**message)
    welcome.timestamp = updated_message['ts']

# @app.route('/message-count', methods=['POST'])
# def message_count():
#     data = request.form
#     user_id = data.get('user_id')
#     channel_id = data.get('channel_id')
#     message_count = message_counts.get(user_id, 0)
#     bot_client.chat_postMessage(channel=channel_id, text=f"Message: {message_count}")
#     return Response(), 200

@app.route('/speak', methods=['POST'])
def speakcommand():
    speak()
    return Response(), 200



@app.route('/slack/interactivity', methods=['POST'])
def interactivity():
    data = request.form
    payload = json.loads(data.get('payload'))
    user_id = payload['user']['id']
    channel_id = payload['channel']['id']
    action_id = payload['actions'][0]['action_id']
    actions = payload['actions'][0]
    actions_value = payload['actions'][0] ['selected_option'] ['value']
    print(user_id)
    # print(actions_value)
    # print(action_id)
    if actions_value == "mechanical":
        # client.channel_invite(channel='C04KARSQMAM', users=user_id, force= false) #invites user to #announcement channel
        # client.conversations_invite(channel='C073U8MUTAM', users=user_id, force= false) #invites user to #general channel 
        client.conversations_invite(channel='C060C6E875M', users=user_id) #invites user to #mechanical-subteam channel 
    elif actions_value == "cad":
        # client.conversations_invite(channel='C04KARSQMAM', users=user_id, force= false) #invites user to #announcement channel
        # client.conversations_invite(channel='C073U8MUTAM', users=user_id, force= false) #invites user to #general channel
        client.conversations_invite(channel='C060C92R37H', users=user_id) #invites user to #mechanical-cad-subteam channel 
    elif actions_value == "programming":
        # client.conversations_invite(channel='C04KARSQMAM', users=user_id) #invites user to #announcement channel
        # client.conversations_invite(channel='C073U8MUTAM', users=user_id) #invites user to #general channel
        client.conversations_invite(channel='C060C5BTE4X', users=user_id) #invites user to #programming-sub-team channel
    elif actions_value == "electrical":
        # client.conversations_invite(channel='C04KARSQMAM', users=user_id) #invites user to #announcement channel
        # client.conversations_invite(channel='C073U8MUTAM', users=user_id) #invites user to #general channel
        client.conversations_invite(channel='C04JK5YC20P', users=user_id) #invites user to #electrical channel
    elif actions_value == "media":
        # client.conversations_invite(channel='C04KARSQMAM', users=user_id) #invites user to #announcement channel
        # client.conversations_invite(channel='C073U8MUTAM', users=user_id) #invites user to #general channel
        client.conversations_invite(channel='C060L2JGG6S', users=user_id) #invites user to #communication-subteam channel
    return Response(), 200


if __name__ == "__main__":
    app.run(debug=True)