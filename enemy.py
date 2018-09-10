import time
import random
import re
from environment import Enemy_Bullet


class Enemy():

    def __init__(self, x, y, ld, ll, lr, grid, trigger):
        self.limit_down = ld
        self.limit_left = ll
        self.limit_right = lr
        self.grid = grid
        self.y = y
        self.x = x
        self.dir = 1
        self.type = 0
        self.trigger = trigger
        self.flag = 0

    def remove(self):
        self.grid[self.y][self.x] = ' '

    def check_collision(self, player_posx, player_posy):
        if (self.x == player_posx + 1 or self.x ==
                player_posx) and self.y == player_posy + 2:
            self.remove()
            return 1
        elif (self.x == player_posx or self.x == player_posx + 1) and (player_posy == self.y or player_posy == self.y - 1):
            return 2

    def gravity_check(self, player_x):
        if player_x >= self.trigger:
            self.flag = 1
        else:
            pass
        if self.flag != 0 and re.match(
                r'[\sOMLEFS_()]', self.grid[self.y + 1][self.x]) is not None:
            self.remove()
            self.y += 1
            self.put()


class Basic_Enemy(Enemy):

    def __init__(self, x, y, ld, ll, lr, grid, trigger):
        super().__init__(x, y, ld, ll, lr, grid, trigger)
        self.type = 1
        self.vel = 1

    def put(self):
        self.grid[self.y][self.x] = 'E'

    def move(self):
        self.remove()
        if re.match(r'[X*]', self.grid[self.y][self.x + self.vel * self.dir]) is not None or (
                self.y == self.limit_down and self.grid[self.y + 1][self.x + 1] == ' '):
            self.dir *= -1
        self.x += self.vel * self.dir
        self.put()


class Shooting_Enemy(Enemy):

    def __init__(self, x, y, ld, ll, lr, grid, trigger):
        super().__init__(x, y, ld, ll, lr, grid, trigger)
        self.type = 2
        self.vel = 1
        self.cur1 = 0

    def put(self):
        self.grid[self.y][self.x] = 'S'

    def move(self, player_x, arr):
        if time.time() - self.cur1 >= 1:
            self.cur1 = time.time()
            arr.append(
                Enemy_Bullet(
                    self.x,
                    self.y,
                    self.dir * -1,
                    self.limit_down,
                    self.limit_left,
                    self.limit_right,
                    self.grid))
            arr[-1].put()
            self.remove()
            if re.match(r'[X*]', self.grid[self.y][self.x + self.vel * self.dir]) is not None or (
                    self.y == self.limit_down and self.grid[self.y + 1][self.x + 1] == ' '):
                self.dir *= -1
            self.x += self.vel * self.dir
        self.put()


class Smart_Enemy(Enemy):

    def __init__(self, x, y, ld, ll, lr, grid, trigger):
        super().__init__(x, y, ld, ll, lr, grid, trigger)
        self.type = 3
        self.vel = 1
        self.cur1 = 0
        self.dir = 1

    def put(self):
        self.grid[self.y][self.x] = 'F'

    def move(self, player_x):
        if time.time() - self.cur1 >= 0.7:
            self.cur1 = time.time()
            self.remove()
            self.dir = 0 if (
                player_x - self.x) == 0 else int((player_x - self.x) / abs(player_x - self.x))
            if self.grid[self.y +
                         1][self.x] == ' ' or (re.match(r'[X*]', self.grid[self.y][self.x +
                                                                                   self.vel *
                                                                                   self.dir]) is not None or (self.y == self.limit_down and self.grid[self.y +
                                                                                                                                                      1][self.x +
                                                                                                                                                         1] == ' ')):
                pass
            else:
                self.x += self.dir * self.vel
        self.put()
