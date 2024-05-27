from flask import Flask
from slackeventsapi import SlackEventAdapter
import os
from config import load_environment
from handlers import register_event_handlers, init_slack_clients, get_bot_id

# Load environment variables
load_environment()

# Create Flask app and Slack event adapter
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ["SIGNING_SECRET"], "/slack/events", app)
client, bot_client = init_slack_clients()
BOT_ID = get_bot_id(bot_client)

# Register event handlers
register_event_handlers(slack_event_adapter, client, bot_client, BOT_ID)

if __name__ == "__main__":
    app.run(debug=True)
