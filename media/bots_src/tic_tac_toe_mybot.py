

class Bot:
    def get_step(self, current_field):
        while True:
            bot_choose = randint(0, 8)
            if current_field[bot_choose] == -1:
                return bot_choose
