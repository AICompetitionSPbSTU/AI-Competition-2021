from random import randint
# TIC TAC TOE GAME FILE!!!!
# По хорошему нужно писать проверку условий победы, но коль у лизы они уже написаны предлагаю забить
from random import seed, randint


class Game:

    def __init__(self, *, bot, state=None):
        if not state:
            self.state = dict()
            self.state['field'] = [-1 for _ in range(9)]
        else:
            print(state)
            self.state = state
        self.bot = bot

    def get_state(self):
        return self.state

    def start_game(self):
        seed()
        self.state['turn'] = 'bot' if randint(0, 1) == 0 else 'user'

    def check_game_state(self):
        pass

    def bot_move(self):
        # print(self.state['number'])
        self.change_state_field(self.bot.get_step(self.state['field']), 0)
        # if self.state['field'] != 1:
        self.change_state_turn('user')
        self.check_game_state()

    def user_move(self, field_pos):
        self.change_state_field(field_pos, 1)
        self.check_game_state()
        # if self.state['field'] != 1:
        self.change_state_turn('bot')

    #     else win!!!

    def change_state_turn(self, player):
        self.state['turn'] = player

    def change_state_field(self, field_pos, change_by):
        self.state['field'][field_pos] = change_by

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
