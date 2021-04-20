from bot import MatchesBot


class MyBot(MatchesBot):
    @staticmethod
    def get_matches_number(current_number):
        return 2
