from matches import MatchesGame
from bot_matches import MatchesBot
import sys

#
# import os
# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)

game = MatchesGame(bot=MatchesBot)
game.start_game()

print("lets go")

i = 0

while True:
##    state = game.get_current_state()
##    if state['turn'] == 'bot':
##        game.bot_move()
##    elif state['turn'] == 'user':
##        game.user_input(number_chosen=2) # то, что получаем от user'а

    sys.stdout.write(f'line #{i}: ' + sys.stdin.readline())
    sys.stdout.flush()

    i += 1

## print(game.get_winner())
