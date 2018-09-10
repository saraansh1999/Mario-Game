from enemy import *
from environment import *
from collectibles import *
import random


class Maker():

    def __init__(self):
        self.arr = []

    def __call__(self):
        return self.arr


class Pipe_Maker(Maker):

    def __init__(self, pos, base_bottom, base_left, base_right, grid):
        super().__init__()
        for i in [(10, 3), (30, 3), (55, 3), (75, 3), (110, 3), (130, 3), (155, 3), (175, 3),
                  (222, 3), (230, 5), (238, 7), (246, 5), (254, 3), (280, 3), (286, 5), (322, 3), (328, 5)]:
            self.arr.append(
                Pipe(
                    i[0],
                    i[1],
                    base_bottom,
                    base_left,
                    base_right,
                    grid))
            self.arr[-1].put()


class Enemy_Maker(Maker):

    def __init__(self, base_bottom, base_left, base_right, grid):
        super().__init__()
        for i in [
            (20,
             base_bottom,
             1,
             0),
            (65,
             base_bottom,
             1,
             0),
            (120,
             base_bottom,
             1,
             0),
            (165,
             base_bottom,
             1,
             0),
            (176,
             3,
             3,
             182),
            (206,
             3,
             3,
             182),
            (270,
             base_bottom,
             2,
             0),
            (290,
             3,
             3,
             0),
            (294,
             base_bottom,
             2,
             0),
            (330,
             3,
             3,
             0),
            (228,
             base_bottom,
             1,
             0)]:
            if i[2] == 1:
                self.arr.append(
                    Basic_Enemy(
                        i[0],
                        i[1],
                        base_bottom,
                        base_left,
                        base_right,
                        grid,
                        i[3]))
            elif i[2] == 2:
                self.arr.append(
                    Shooting_Enemy(
                        i[0],
                        i[1],
                        base_bottom,
                        base_left,
                        base_right,
                        grid,
                        i[3]))
            else:
                self.arr.append(
                    Smart_Enemy(
                        i[0],
                        i[1],
                        base_bottom,
                        base_left,
                        base_right,
                        grid,
                        i[3]))
            self.arr[-1].put()


class Brick_Maker(Maker):

    def __init__(self, base_bottom, base_left, base_right, grid):
        super().__init__()
        for i in [(82, 5), (88, 8), (94, 5), (176, 16), (182, 5), (182, 12), (188, 8), (194, 5),
                  (194, 12), (200, 16), (215, 8), (343, 32), (355, 24), (367, 16), (379, 8)]:
            self.arr.append(
                Brick(
                    i[0],
                    i[1],
                    base_bottom,
                    base_left,
                    base_right,
                    grid))
            self.arr[-1].put()


class Moving_Brick_Maker(Maker):
    def __init__(self, base_bottom, base_left, base_right, grid):
        super().__init__()
        for i in [(335, 5)]:
            self.arr.append(
                Moving_Brick(
                    i[0],
                    i[1],
                    base_bottom,
                    base_left,
                    base_right,
                    grid,
                    30))
            self.arr[-1].put()


class Pit_Maker(Maker):

    def __init__(
            self,
            pos,
            base_bottom,
            base_left,
            base_right,
            grid,
            border_bottom):
        super().__init__()
        for i in [(81, 22), (181, 40), (343, 45)]:
            self.arr.append(Pit(i[0],
                                i[1],
                                base_bottom,
                                base_left,
                                base_right,
                                grid,
                                base_bottom + 1,
                                border_bottom - 1))
            self.arr[-1].put()


class Coin_Maker(Maker):

    def __init__(self, bb, grid):
        super().__init__()
        list = []
        list.extend((36 + j, bb - 5) for j in range(5, 15))
        list.extend((83 + j, bb - 5) for j in range(0, 5))
        list.extend((95 + j, bb - 5) for j in range(0, 5))
        list.extend((136 + j, bb - 6) for j in range(5, 15))
        list.extend((183 + j, bb - 5) for j in range(0, 5))
        list.extend((195 + j, bb - 5) for j in range(0, 5))
        list.extend((177 + j, bb - 16) for j in range(0, 5))
        list.extend((201 + j, bb - 16) for j in range(0, 5))
        list.extend((252, bb + 1 - j) for j in range(0, 3))
        list.extend((253, bb + 1 - j) for j in range(0, 3))
        list.extend((236 + j, bb - 19) for j in range(0, 2))
        list.extend((244 + j, bb - 19) for j in range(0, 2))
        for i in list:
            self.arr.append(Coins(i[0], i[1], grid))
            self.arr[-1].put()


class Gun_Upgrade_Maker(Maker):

    def __init__(self, bb, grid):
        super().__init__()
        for i in [(92, bb - 12, 2), (241, bb - 12, 2), (410, bb - 7, 3)]:
            self.arr.append(Gun(i[0], i[1], grid, i[2]))
            self.arr[-1].put()


class Cloud_Maker(Maker):
    def __init__(self, bt, width, base_bottom, base_left, base_right, grid):
        super().__init__()
        for i in range(3, width, 40):
            self.arr.append(
                Cloud(
                    i,
                    random.randint(
                        bt + 3,
                        bt + 8),
                    base_bottom,
                    base_left,
                    base_right,
                    grid))
            self.arr[-1].put()


class Spring_Maker(Maker):
    def __init__(self, base_bottom, base_left, base_right, grid):
        super().__init__()
        for i in [236, 237, 244, 245]:
            self.arr.append(
                Spring(
                    i,
                    base_bottom,
                    base_left,
                    base_right,
                    grid))
            self.arr[-1].put()
