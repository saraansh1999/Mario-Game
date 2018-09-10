import re
import time
import random
from environment import Boss_Bullet


class Boss():

    def __init__(self, x, y, lu, ld, ll, lr, grid):
        self.x = x
        self.y = y
        self.limit_up = lu
        self.limit_down = ld
        self.limit_left = ll
        self.limit_right = lr
        self.grid = grid
        self.dir = 0
        self.lives = 10
        self.last_jump = 0
        self.last_horizontal_move = 0
        self.last_shoot = 0
        self.vel = 1
        self.disha = 2

    def put(self, ch):
        self.grid[self.y][self.x] = 'B'
        self.grid[self.y + 1][self.x] = 'B'
        self.grid[self.y + 2][self.x] = 'B'
        self.grid[self.y + 3][self.x] = 'B'
        self.grid[self.y][self.x + 1] = 'B'
        self.grid[self.y + 1][self.x + 1] = 'B'
        self.grid[self.y + 2][self.x + 1] = 'B'
        self.grid[self.y + 3][self.x + 1] = 'B'
        if ch == 1:
            self.dir = 0

    def remove(self):
        self.grid[self.y][self.x] = ' '
        self.grid[self.y + 1][self.x] = ' '
        self.grid[self.y + 2][self.x] = ' '
        self.grid[self.y + 3][self.x] = ' '
        self.grid[self.y][self.x + 1] = ' '
        self.grid[self.y + 1][self.x + 1] = ' '
        self.grid[self.y + 2][self.x + 1] = ' '
        self.grid[self.y + 3][self.x + 1] = ' '

    def move(self, dir):

        #1 is up , 2 is left , 3 is right

        self.remove()

        if dir == 1:
            self.dir = 1
            f = 0
            i = 0
            for i in list(range(self.y - 5, self.y))[::-1]:
                # if self.grid[i][self.x]!=' ':
                if re.match(r'[\sOGML]', self.grid[i][self.x]) is None or re.match(
                        r'[\sGOML]', self.grid[i][self.x + 1]) is None:
                    self.y -= (-i + self.y - 1)
                    f += 1
                    break
            if f == 0:
                self.y -= 5
                return 5
            else:
                return self.y - i - 1
        if dir == 2:
            if re.match(r'[\sOGML]', self.grid[self.y][self.x -
                                                       1]) is not None and re.match(r'[\sOGML]', self.grid[self.y +
                                                                                                           1][self.x -
                                                                                                              1]) is not None and re.match(r'[\sOG]', self.grid[self.y +
                                                                                                                                                                2][self.x -
                                                                                                                                                                   1]) is not None and re.match(r'[\sOG]', self.grid[self.y +
                                                                                                                                                                                                                     3][self.x -
                                                                                                                                                                                                                        1]) is not None and self.x > self.limit_left:
                self.x -= 1
            self.dir = 2
        if dir == 3:
            if re.match(r'[\sOGML]', self.grid[self.y][self.x +
                                                       2]) is not None and re.match(r'[\sOGML]', self.grid[self.y +
                                                                                                           1][self.x +
                                                                                                              2]) is not None and re.match(r'[\sOG]', self.grid[self.y +
                                                                                                                                                                2][self.x +
                                                                                                                                                                   2]) is not None and re.match(r'[\sOG]', self.grid[self.y +
                                                                                                                                                                                                                     3][self.x +
                                                                                                                                                                                                                        2]) is not None and self.x < self.limit_right:
                self.x += 1
            self.dir = 3

        self.put(0)

    def gravity_check(self):
        if re.match(r'[\sEOGSFML_()]',
                    self.grid[self.y + 4][self.x]) is not None and re.match(r'[\sEOGSFML_()]',
                                                                            self.grid[self.y + 4][self.x + 1]) is not None:
            self.remove()
            self.y += 1
            self.put(0)
            return 0
        else:
            return 1

    def die(self):
        if self.lives > 0:
            self.lives -= 1
            return 0
        else:
            self.remove()
            return 1

    def random_jump(self, can):
        if time.time() - self.last_jump >= 1:
            self.last_jump = time.time()
            if can == 1:
                self.move(1)

    def horizontal_move(self):
        if time.time() - self.last_horizontal_move >= 1:
            self.remove()
            self.last_horizontal_move = time.time()
            if self.x == self.limit_left:
                self.disha = 3
            if self.x == self.limit_right - 1:
                self.disha = 2
            self.move(self.disha)
        self.put(0)

    def shoot(self, arr, player_x):
        if time.time() - self.last_shoot >= 2.5:
            self.last_shoot = time.time()
            arr.append(
                Boss_Bullet(
                    self.x - 1,
                    self.y + 2,
                    1 if player_x > self.x else -1,
                    self.limit_down,
                    self.limit_left,
                    self.limit_right,
                    self.grid))
            arr[-1].put()
            arr.append(
                Boss_Bullet(
                    self.x - 1,
                    self.y + 3,
                    1 if player_x > self.x else -1,
                    self.limit_down,
                    self.limit_left,
                    self.limit_right,
                    self.grid))
            arr[-1].put()

    def check_collision(self, player_x, player_y):
        if (player_x in [self.x + i for i in range(-1, 2)]
                ) and (player_y in [self.y + i for i in range(-1, 4)]):
            return 1
        else:
            return 0
