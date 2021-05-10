# Example bot for tic_tac_toe game
# Use the class and functions shown in your implementations to influence the game process
# Your built-in functions
#  math, __build_class__, randint  ,range,  len
# Dont try to use your power to violate the game-laws, or your bot will be punished!

class Bot:
    def get_step(self, current_field):
        """
        current_field: list[9] of int where -1 is free to use, 0 is bot choose, 1 is player
        ---
        return int number from 0 to 8 where you choose to put 0.
        """
        while True:
            bot_choose = randint(0, 8)
            if current_field[bot_choose] == -1:
                return bot_choose
