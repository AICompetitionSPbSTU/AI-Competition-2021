from media.game_src.matches import MatchesGame
from media.game_src.bot_matches import MatchesBot
#
# import os
# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)

game = MatchesGame(bot=MatchesBot)
game.start_game()
print("lets go")
while not game.get_winner():
    state = game.get_current_state()
    if state['turn'] == 'bot':
        game.bot_move()
    elif state['turn'] == 'user':
        game.user_input(number_chosen=2) # то, что получаем от user'а
print(game.get_winner())