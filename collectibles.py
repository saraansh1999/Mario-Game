class Collectibles():

    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid
        self.vel = 1
        self.collected = 0

    def remove(self):
        self.grid[self.y][self.x] = ' '

    def check_collection(self, player_posx, player_posy):
        if (self.x == player_posx or self.x == player_posx +
                1) and (self.y == player_posy or self.y == player_posy + 1):
            if type == 1:
                self.remove()
            return 1
        else:
            self.put()
            return 0

    def check_collection_jump(self, player_posx, player_posy, jump):
        for i in range(0, jump):
            if (self.x == player_posx or self.x ==
                    player_posx + 1) and self.y == player_posy + i:
                if self.type == 1 or self.type == 2:
                    self.remove()
                return 1
            else:
                self.put()


class Coins(Collectibles):

    def __init__(self, x, y, grid):
        super().__init__(x, y, grid)
        self.type = 1

    def put(self):
        self.grid[self.y][self.x] = 'O'


class Gun(Collectibles):

    def __init__(self, x, y, grid, type):
        super().__init__(x, y, grid)
        self.type = type

    def put(self):
        self.grid[self.y][self.x] = 'G'
