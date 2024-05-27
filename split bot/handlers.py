import slack
import os
import string
from flask import app, request, Response
from welcome import send_welcome_message

BAD_WORDS = []

def init_slack_clients():
    client = slack.WebClient(token=os.environ['SLACK_USER_TOKEN'])
    bot_client = slack.WebClient(token=os.environ['SLACK_BOT_TOKEN'])
    return client, bot_client

def get_bot_id(bot_client):
    return bot_client.api_call("auth.test")['user_id']

def check_if_bad_words(message):
    msg = message.lower()
    msg = msg.translate(str.maketrans('', '', string.punctuation))
    return any(word in msg for word in BAD_WORDS)

def register_event_handlers(slack_event_adapter, client, bot_client, BOT_ID):
    WelcomeMessages = {}
    message_counts = {}
    whitelisted_users = [
        "U06031QSBSB", "U0607TBATL3", "U04KMTN3JC8", "U04KHFCTMUH", "U04JYH0TXQS",
        "U060FS0PXGU", "U04KN83QUN4", "U04KB68EULR", "U0603URJGDT", "U04JRURDZSA",
        "U060L9L613Q", "U060KGX8RA5", "U0600QD62EA", BOT_ID, None
    ]
    speakCommandWhitelist = os.environ['SPEAK_COMMAND_WHITELIST']
    messages_set = set()
    ts_to_delete = set()

    @slack_event_adapter.on('message')
    def message(payload):
        event = payload.get("event", {})
        channel_id = event.get("channel")
        user_id = event.get("user")
        text = event.get("text")
        timestamp = event.get("ts")
        if user_id and BOT_ID != user_id:
            if user_id in message_counts:
                message_counts[user_id] += 1
            else:
                message_counts[user_id] = 1
            if text.lower() == 'welcome_message.test':
                send_welcome_message(bot_client, WelcomeMessages, f'@{user_id}', user_id)
            elif check_if_bad_words(text):
                ts = event.get('ts')
                bot_client.chat_postMessage(channel=channel_id, thread_ts=ts, text="That is a bad word!(TESTING)")
        if len(text) == 1:
            client.chat_delete(channel=channel_id, ts=timestamp)
        elif not user_id in whitelisted_users and channel_id == "C04KARSQMAM":
            messages_set.add(timestamp)
            for ts in messages_set:
                ts_to_delete.add(ts)
                try:
                    client.chat_delete(channel=channel_id, ts=ts)
                except Exception:
                    pass
            try:
                while messages_set:
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
            send_welcome_message(bot_client, WelcomeMessages, f'@{user_id}', user_id)

    @slack_event_adapter.on('reaction_added')
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

    @app.route('/speak', methods=['POST'])
    def speak():
        data = request.form
        user_id = data.get('user_id')
        channel_id = data.get('channel_id')
        text = data.get('text')
        if user_id in speakCommandWhitelist:
            bot_client.chat_postMessage(channel=channel_id, text=text)
            return Response(), 200
        else:
            return Response(), 200
