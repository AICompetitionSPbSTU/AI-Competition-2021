from random import seed, randint


# MATCHES GAME FILE

class Game:

    def __init__(self, *, bot, state=None):
        if not state:
            self.state = dict()
            self.state['field'] = 21
        else:
            print(state)
            self.state = state
        self.bot = bot

    def get_state(self):
        return self.state['field']

    def start_game(self):
        seed()
        self.state['turn'] = 'bot' if randint(0, 1) == 0 else 'user'

    def bot_move(self):
        # print(self.state['number'])
        self.change_state_matches(self.bot.get_matches_number(self.state['field']))
        if self.state['field'] != 1:
            self.change_state_turn('user')

    def user_move(self, matches_number):
        self.change_state_matches(matches_number)
        if self.state['field'] != 1:
            self.change_state_turn('bot')

    #     else win!!!

    def change_state_turn(self, player):
        self.state['turn'] = player

    def change_state_matches(self, matches_number):
        change = int(matches_number)
        if 0 < change < 4:
            self.state['field'] = self.state['field'] - change
        else:  # cheating from bot i guess
            self.state['field'] = 2  # user will win

    def user_input(self, **kwargs):
        if 'user_action' in kwargs:
            self.user_move(kwargs['user_action'])
        else:
            raise BaseException('You didn`t choose matches number')

    def get_winner(self):
        if self.state['field'] == 1:
            return self.state['turn']
        else:
            return False
