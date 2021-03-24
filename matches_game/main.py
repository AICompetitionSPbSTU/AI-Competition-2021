from matches import MatchesGame
from mybot import MyBot

game = MatchesGame(bot=MyBot)
game.start_game()
while not game.get_winner():
    state = game.get_current_state()
    if state['turn'] == 'bot':
        game.bot_move()
    elif state['turn'] == 'user':
        game.user_input(number_chosen=2) # то, что получаем от user'а
print(game.get_winner())