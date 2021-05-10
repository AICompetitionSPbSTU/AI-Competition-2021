# Example bot for pacman game
# Use the class and functions shown in your implementations to influence the game process
# Your built-in functions
#  math, __build_class__, randint  ,range,  len
# Dont try to use your power to violate the game-laws, or your bot will be punished!



class Bot:

    def move(self, state):
        """
        map: 2d array of 1 and 'C',where 1 - is wall, 'C' - coins
        pp : list of [x,y] coordinate of player_pos
        bp : list of [x,y] coordinate of bot_pos
        ps : int players score
        bs : int bot score
        ---
        return 'left','up','right','down'
        """
        map_ = state['map']
        player_pos = state['pp']
        bot_pos = state['bp']
        player_score = state['ps']
        bot_score = state['bs']
        dir_to_player_y = player_pos[0] - bot_pos[0]
        dir_to_player_x = player_pos[1] - bot_pos[1]
        if dir_to_player_y < 0:  # player is higher
            if self.no_wall(map_, bot_pos, "up"):
                return "up"
        elif dir_to_player_y > 0:
            if self.no_wall(map_, bot_pos, "down"):
                return "down"
        if dir_to_player_x > 0:
            if self.no_wall(map_, bot_pos, "right"):
                return "right"
        elif dir_to_player_x < 0:
            if self.no_wall(map_, bot_pos, "left"):
                return "left"
        random_dir = randint(0, 3)
        if random_dir == 0:
            if self.no_wall(map_, bot_pos, "left"):
                return "left"
        elif random_dir == 1:
            if self.no_wall(map_, bot_pos, "up"):
                return "up"
        elif random_dir == 2:
            if self.no_wall(map_, bot_pos, "right"):
                return "right"
        else:
            if self.no_wall(map_, bot_pos, "down"):
                return "down"

        return "up"

    def no_wall(self, map, pos, action):
        move = self.action_to_move(action)
        new_player_pos = [pos[0] + move[0],
                          pos[1] + move[1]]
        return map[new_player_pos[0]][new_player_pos[1]] != '1'

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
