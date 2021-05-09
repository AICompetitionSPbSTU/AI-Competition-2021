PLAYER_START_POS = (1, 1)
BOT_START_POS = (29, 26)


def load_map():
    map_ = None
    with open('media/game_src/pacman/walls.txt', 'r') as f:
        lines = f.readlines()
        map_ = list(map(lambda s: list(s[:-1]), lines[:-1]))
        map_.append(list(lines[-1]))
    assert map_

    return map_


class Game:

    def __init__(self, bot, state=None):
        self.bot = bot

        if not state is None:
            global load_map
            self.map_ = state['map']
            self.player_pos = state['pp']
            self.bot_pos = state['bp']
            self.player_score = state['ps']
            self.bot_score = state['bs']

    def start_game(self):
        global load_map, PLAYER_START_POS, BOT_START_POS
        self.map_ = load_map()
        self.player_pos = list(PLAYER_START_POS)
        self.bot_pos = list(BOT_START_POS)
        self.player_score = 0
        self.bot_score = 0

    def get_winner(self):
        for row in self.map_:
            for cell in row:
                if cell == 'C':
                    return 'none'
        if self.player_score > self.bot_score:
            return 'player'
        elif self.player_score < self.bot_score:
            return 'bot'
        else:
            return 'draw'

    def get_state(self):
        state = {'pp': self.player_pos,
                 'bp': self.bot_pos,
                 'ps': self.player_score,
                 'bs': self.bot_score,
                 'map': self.map_,
                 'winner': self.get_winner()}
        return state

    def action_to_move(self, action):
        if action == 'up':
            move = [-1, 0]
        elif action == 'down':
            move = [1, 0]
        elif action == 'left':
            move = [0, -1]
        elif action == 'right':
            move = [0, 1]
        else:
            move = None
        return move

    def in_bounds(self, pos):
        return 0 <= pos[0] < len(self.map_) and 0 <= pos[1] < len(self.map_[0])

    def no_wall(self, pos):
        return self.map_[pos[0]][pos[1]] != '1'

    def is_coin(self, pos):
        return self.map_[pos[0]][pos[1]] == 'C'

    def user_input(self, user_action):
        assert hasattr(self, 'map_'), 'game not started'
        
        player_move = self.action_to_move(user_action)
        assert player_move

        new_player_pos = [self.player_pos[0] + player_move[0],
                          self.player_pos[1] + player_move[1]]

        if self.in_bounds(new_player_pos) and self.no_wall(new_player_pos):
            if self.is_coin(new_player_pos):
                self.map_[new_player_pos[0]][new_player_pos[1]] = ' '
                self.player_score += 1
            self.player_pos = new_player_pos

    def bot_move(self):
        assert hasattr(self, 'map_'), 'game not started'
        
        bot_action = self.bot.move(self.get_state().copy())
        bot_move = self.action_to_move(bot_action)

        new_bot_pos = [self.bot_pos[0] + bot_move[0],
                       self.bot_pos[1] + bot_move[1]]

        if self.in_bounds(new_bot_pos) and self.no_wall(new_bot_pos):
            if self.is_coin(new_bot_pos):
                self.map_[new_bot_pos[0]][new_bot_pos[1]] = ' '
                self.bot_score += 1
            self.bot_pos = new_bot_pos
        

        
