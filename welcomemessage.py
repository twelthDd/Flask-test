#* class containing the welcome message sent to user when they join the server (Noah)
class WelcomeMessage:
    
    START_TEXT = {
        'type': 'section',
        'text': {
        'type': 'mrkdwn',
        'text': (
            'Welcome to the Villaciraptors Slack HQ, Team 9076! :gear: \n\n '
           ' Hey there, rookie or veteran, I am your friendly neighborhood robotics bot! \n\n '
           'To get started and join your subteam channels, Please select which subteam you would like to join: \n\n'
           ":gear: Mechanical Team - for building and maintaining the robot's mechanisms \n"
           ':triangular_ruler: CAD Team - designes the robot at the beguining of each game with the help of cad (computer aided design) \n'
           ":computer: Programming Team - for coding and controlling the robot's brain \n"
           ":electric_plug: Electrical Team - for wiring, power distribution, and electrical systems \n"
           ":camera: Media/communications Team - for social media and sponsorship primarily \n\n"
           "Let's make this season a roaring success! :tada: \n\n"
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
        text = 'Select a subteam channel to join: ------->'

        return {
            'type': 'section',
            'text': {
            'type': 'mrkdwn',
            'text': text
            },
            'accessory': {
            'type': 'static_select',
            'placeholder': {
                'type': 'plain_text',
                'text': 'Select a subteam channel'
            },
            'options': [
                {
                'text': {
                    'type': 'plain_text',
                    'text': 'mechanical Team'
                },
                'value': 'mechanical'
                },
                {
                'text': {
                    'type': 'plain_text',
                    'text': 'CAD Team'
                },
                'value': 'cad'
                },
                {
                'text': {
                    'type': 'plain_text',
                    'text': 'Programming Team'
                },
                'value': 'programming'
                },
                {
                'text': {
                    'type': 'plain_text',
                    'text': 'Electrical Team'
                },
                'value': 'electrical'
                },
                {
                'text': {
                    'type': 'plain_text',
                    'text': 'Media/communications Team'
                },
                'value': 'media'
                }
            ]
            }
        }

        def add_member_to_channel(self, subteam):
            # Add logic here to add the member to the selected subteam channel
            if subteam == 'mechanisms':
                # Add code to add member to Mechanical Team channel
                pass
            elif subteam == 'programming':
                # Add code to add member to Programming Team channel
                pass
            elif subteam == 'electrical':
                # Add code to add member to Electrical Team channel
                pass
            elif subteam == 'media':
                # Add code to add member to Media/communications Team channel
                pass
            else:
                # Handle invalid subteam selection
                pass