import slack

class WelcomeMessage:
    START_TEXT = {
        'type': 'section',
        'text': {
            'type': 'mrkdwn',
            'text': (
                'Welcome to this awesome channel! \n\n'
                '*Get started by completing some tasks*'
            )}
    }
    DIVIDER = {'type': 'divider'}
    
    def __init__(self, channel, user):
        self.channel = channel
        self.user = user
        self.icon_emoji = ':robot_face:'
        self.timestamp = ''
        self.completed = False

    def get_message(self):
        return {
            'ts': self.timestamp,
            'channel': self.channel,
            'username': 'Welcome Robot!',
            'icon_emoji': self.icon_emoji,
            'blocks': [
                self.START_TEXT,
                self.DIVIDER,
                self._get_reaction_task()
            ]
        }
        
    def _get_reaction_task(self):
        checkmark = ':white_check_mark:'
        if not self.completed:
            checkmark = ':white_large_square:'
        text = f'{checkmark} *React to this message!*'
        return {'type': 'section', 'text': {'type': 'mrkdwn', 'text': text}}

def send_welcome_message(bot_client, WelcomeMessages, channel, user):
    if channel not in WelcomeMessages:
        WelcomeMessages[channel] = {}
    if user in WelcomeMessages[channel]:
        return
    welcome = WelcomeMessage(channel, user)
    message = welcome.get_message()
    response = bot_client.chat_postMessage(**message)
    welcome.timestamp = response['ts']
    WelcomeMessages[channel][user] = welcome
