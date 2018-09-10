import time
import random
import re


class Elements():

    def __init__(self, ld, ll, lr, grid):
        self.vel = 1
        self.limit_bottom = ld
        self.limit_left = ll
        self.limit_right = lr
        self.grid = grid


class Spring(Elements):

    def __init__(self, x, ld, ll, lr, grid):
        super().__init__(ld, ll, lr, grid)
        self.x = x
        self.y = self.limit_bottom

    def put(self):
        self.grid[self.y][self.x] = '8'

    def check_application(self, player_x, player_y):
        if (self.x == player_x or self.x ==
                player_x + 1) and player_y == self.y - 1:
            return 1
        else:
            return 0


class Pipe(Elements):

    def __init__(self, x, height, ld, ll, lr, grid):
        super().__init__(ld, ll, lr, grid)
        self.height = height
        self.width = 5
        self.x = x
        self.y = self.limit_bottom - self.height

    def put(self):
        for i in range(self.y, self.limit_bottom + 1):
            if self.x >= self.limit_left:
                self.grid[i][self.x] = '*'
            if self.x + self.width >= self.limit_left:
                self.grid[i][self.x + self.width] = '*'
        for i in range(self.x, self.x + self.width + 1):
            if i >= self.limit_left:
                self.grid[self.y][i] = '*'

    def remove(self):
        for i in range(self.y, self.limit_bottom + 1):
            if self.x >= self.limit_left:
                self.grid[i][self.x] = ' '
            if self.x + self.width >= self.limit_left:
                self.grid[i][self.x + self.width] = ' '
        for i in range(self.x, self.x + self.width + 1):
            if i >= self.limit_left:
                self.grid[self.y][i] = ' '


class Brick(Elements):

    def __init__(self, x, y, ld, ll, lr, grid):
        super().__init__(ld, ll, lr, grid)
        self.height = y
        self.width = 6
        self.x = x
        self.y = self.limit_bottom - self.height
        self.grid = grid

    def put(self):
        for i in range(self.x, self.x + self.width + 1):
            if i >= self.limit_left and i <= self.limit_right:
                self.grid[self.y][i] = 'X'

    def remove(self):
        for i in range(self.x, self.x + self.width + 1):
            if i >= self.limit_left and i <= self.limit_right:
                self.grid[self.y][i] = ' '


class Moving_Brick(Brick):

    def __init__(self, x, y, ld, ll, lr, grid, range):
        super().__init__(x, y, ld, ll, lr, grid)
        self.lowery = self.y
        self.uppery = self.y - range
        self.dir = 1
        self.vel = 1

    def move(self):
        self.remove()
        if self.y <= self.uppery or self.y >= self.lowery:
            self.dir *= -1
        self.y += self.dir * self.vel

    def check_player_above(self, player_posx, player_posy):
        if player_posx + 1 >= self.x and player_posx <= self.x + \
                self.width and (player_posy >= self.y - 2) and self.dir == -1 and self.y > self.uppery:
            return 1
        else:
            return 0


class Pit(Elements):

    def __init__(self, x, w, ld, ll, lr, grid, border_top, border_bottom):
        super().__init__(ld, ll, lr, grid)
        self.top = border_top
        self.bottom = border_bottom
        self.width = w
        self.x = x

    def put(self):
        for i in range(self.x, self.x + self.width + 1):
            for j in range(self.top, self.bottom + 1):
                if j - self.top <= 2:
                    self.grid[j][i] = ' '
                else:
                    self.grid[j][i] = '~'

    def remove(self):
        for i in range(self.x, self.x + self.width + 1):
            for j in range(self.top, self.bottom + 1):
                self.grid[j][i] = 'X'

    def pitfall(self, player_posx, player_posy):
        f = 0
        for i in range(self.x, self.x + self.width + 1):
            if player_posx == i and player_posy > self.limit_bottom:
                f += 1
                return 1
        if f == 0:
            return 0


class Bullet(Elements):

    def __init__(self, posx, posy, vel, ld, ll, lr, grid):
        super().__init__(ld, ll, lr, grid)
        self.x = posx
        self.y = posy
        self.vel = vel

    def put(self):
        self.grid[self.y][self.x] = '-'

    def remove(self):
        self.grid[self.y][self.x] = ' '

    def move(self, start, end):
        self.remove()
        if (re.match(r'[\sEMLSFBO<-=]', self.grid[self.y][self.x +
                                                          self.vel]) is not None) and self.x >= start and self.x <= end:
            self.x = self.x + self.vel
            self.put()
            return 0
        else:
            return 1


class Player_Bullet(Bullet):

    def __init__(self, posx, posy, vel, ld, ll, lr, grid):
        super().__init__(posx, posy, vel, ld, ll, lr, grid)

    def put(self):
        self.grid[self.y][self.x] = '='

    def hitormiss(self, enemyx, enemyy, enemy_type):
        if enemy_type == 1:
            if self.y == enemyy and (
                    self.x + self.vel == enemyx or self.x == enemyx):
                self.remove()
                return 1
            else:
                return 0
        else:
            if (self.y in [enemyy -
                           1, enemyy, enemyy +
                           1, enemyy +
                           2, enemyy +
                           3]) and (self.x == enemyx or self.x +
                                    self.vel == enemyx):
                self.remove()
                return 1
            else:
                return 0


class Enemy_Bullet(Bullet):

    def __init__(self, posx, posy, vel, ld, ll, lr, grid):
        super().__init__(posx, posy, vel, ld, ll, lr, grid)
        self.type = 1

    def put(self):
        self.grid[self.y][self.x] = '-'

    def hitormiss(self, player_posx, player_posy):
        if (self.x == player_posx or self.x == player_posx +
                1) and (self.y == player_posy + 1 or self.y == player_posy):
            self.remove()
            return 1
        else:
            return 0


class Boss_Bullet(Enemy_Bullet):

    def __init__(self, x, y, vel, ld, ll, lr, grid):
        super().__init__(x, y, vel, ld, ll, lr, grid)
        self.type = 2

    def put(self):
        self.grid[self.y][self.x] = '<'


class Cloud(Elements):

    def __init__(self, x, y, ld, ll, lr, grid):
        super().__init__(ld, ll, lr, grid)
        self.x = x
        self.y = y

    def put(self):
        #		 ____  ____
        #		(____)(____)
        #		  (__(____)

        for i in range(0, 4):
            self.grid[self.y][self.x + 1 + i] = '_'
        for i in range(0, 4):
            self.grid[self.y][self.x + 7 + i] = '_'
        for i in range(0, 4):
            self.grid[self.y + 1][self.x + 1 + i] = '_'
        for i in range(0, 4):
            self.grid[self.y + 1][self.x + 7 + i] = '_'
        self.grid[self.y + 1][self.x] = '('
        self.grid[self.y + 1][self.x + 6] = '('
        self.grid[self.y + 1][self.x + 5] = ')'
        self.grid[self.y + 1][self.x + 11] = ')'
        self.grid[self.y + 2][self.x + 2] = '('
        for i in range(0, 2):
            self.grid[self.y + 2][self.x + 3 + i] = '_'
        self.grid[self.y + 2][self.x + 5] = '('
        for i in range(0, 4):
            self.grid[self.y + 2][self.x + 6 + i] = '_'
        self.grid[self.y + 2][self.x + 10] = ')'
