class Scoreboard():

    def __init__(self):
        self.coins = 0
        self.lives = 3
        self.kills = 0
        self.score = 0

    def increment_coins(self):
        self.coins += 1

    def die(self):
        if self.lives > 0:
            self.lives -= 1
            return 0
        else:
            return 1

    def increment_kills(self):
        self.kills += 1

    def update_score(self):
        self.score = self.coins * 5 + self.kills * 20
