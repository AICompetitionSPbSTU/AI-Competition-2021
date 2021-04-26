from random import randint

if game_cond == "start":
    state = ['-1' for _ in range(9)]
else:
    state = state.split(",")
    while True:
        bot_choose = randint(0, 8)
        if state[bot_choose] == '-1':
            state[bot_choose] = '0'
            break
