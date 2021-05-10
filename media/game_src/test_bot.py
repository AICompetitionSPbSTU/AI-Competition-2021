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
            self.state = state
        self.bot = bot

    def get_state(self):
        winner = self.get_winner()
        state = {**self.state, 'winner': winner}
        return state

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
        if self.state['field'][int(field_pos)] == -1:
            self.state['field'][int(field_pos)] = int(change_by)
        else:  # cheating!!!
            self.state['field'] = [1 for _ in range(9)]  # user insta wins

    def user_input(self, **kwargs):
        if 'user_action' in kwargs:
            self.user_move(kwargs['user_action'])
        else:
            raise BaseException('You didn`t choose matches number')

    def get_winner(self):
        print(self.state['field'])
        winCombos = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [6, 4, 2]
        ]
        for cell in self.state['field']:            
            if cell == -1:
                break
        else:
            for combo in winCombos:
                if all(self.state['field'][idx] == 0 for idx in combo):
                    return 'bot'
                if all(self.state['field'][idx] == 1 for idx in combo):
                    return 'player'
            return 'draw'

        for combo in winCombos:
            if all(self.state['field'][idx] == 0 for idx in combo):
                return 'bot'
            if all(self.state['field'][idx] == 1 for idx in combo):
                return 'player'
        return 'none'

    def look_for_combo(self):
        pass
