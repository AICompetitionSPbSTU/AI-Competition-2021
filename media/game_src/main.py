from matches import MatchesGame
from bot_matches import MatchesBot
import sys
from random import  randint
#
# import os
# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)

# game = MatchesGame(bot=MatchesBot)
# game.start_game()


while True:
    state = sys.stdin.readline().split(',')

    bot_choose = randint(0, 8)
    if state[bot_choose] == '-1':
        state[bot_choose] = '0'
        sys.stdout.write(" ".join(state))
        sys.stdout.flush()

#
# sys.stdout.write(f'line #{i}: ' + sys.stdin.readline())
# sys.stdout.flush()

## print(game.get_winner())
