from random import randint

if game_cond == "start":
    state = 21
else:
    bot_choose = randint(1, 3)
    state = int(state) - bot_choose
#
# sys.stdout.write(f'line #{i}: ' + sys.stdin.readline())
# sys.stdout.flush()

## print(game.get_winner())
