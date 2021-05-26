from random import seed, randint


class MatchesGame:
    def __init__(self, *, bot):
        self.state = dict()
        self.state['number'] = 21
        self.bot = bot

    def get_current_state(self):
        return self.state

    def start_game(self):
        seed()
        self.state['turn'] = 'bot' if randint(0, 1) == 0 else 'user'

    def bot_move(self):
        self.change_state_matches(self.bot.get_matches_number(self.state['number']))
        if self.state['number'] != 1:
            self.change_state_turn('user')

    def user_move(self, matches_number):
        self.change_state_matches(matches_number)
        if self.state['number'] != 1:
            self.change_state_turn('bot')

    def change_state_turn(self, player):
        self.state['turn'] = player

    def change_state_matches(self, matches_number):
        self.state['number'] = self.state['number'] - matches_number

    def user_input(self, **kwargs):
        if 'number_chosen' in kwargs:
            self.user_move(kwargs['number_chosen'])
        else:
            raise BaseException('You didn`t choose matches number')

    def get_winner(self):
        if self.state['number'] == 1:
            return self.state['turn']
        else:
            return False
