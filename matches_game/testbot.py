import random

class TestBot(MatchesBot):

    def get_matches_number(self, current_number):
        if current_number <= 4:
            return current_number - 1

        n = current_number - (current_number - 1) // 4 * 4
        
        return n if n > 0 else random.randint(3)
            
            
        4, 5, 6, 7, 8, 9, 10, 11, 12, 13
        +, -, +, +, +, -, +,  +,  +,  -
        1, 5, 9, 13, 17
