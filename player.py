import re


class Player():

    def __init__(self, x, y, lu, ld, ll, lr, grid):
        self.x = x
        self.y = y
        self.limit_up = lu
        self.limit_down = ld
        self.limit_left = ll
        self.limit_right = lr
        self.grid = grid
        self.dir = 0
        self.gun_mode = 0

    def remove(self):
        self.grid[self.y][self.x] = ' '
        self.grid[self.y + 1][self.x] = ' '
        self.grid[self.y][self.x + 1] = ' '
        self.grid[self.y + 1][self.x + 1] = ' '

    def put(self, ch):
        self.grid[self.y][self.x] = 'M'
        self.grid[self.y][self.x + 1] = 'M'
        self.grid[self.y + 1][self.x] = 'L'
        self.grid[self.y + 1][self.x + 1] = 'L'
        if ch == 1:
            self.dir = 0

    def move(self, dir):

        #1 is jump , 2 is left , 3 is right , 4 is move_up

        self.remove()

        if dir == 1:
            self.dir = 1
            f = 0
            i = 0
            for i in list(range(self.y - 7, self.y))[::-1]:
                if re.match(r'[\sOGB]', self.grid[i][self.x]) is None or re.match(
                        r'[\sGOB]', self.grid[i][self.x + 1]) is None:
                    self.y -= (-i + self.y - 1)
                    f += 1
                    break
            if f == 0:
                self.y -= 7
                return 7
            else:
                return self.y - i - 1
        if dir == 2:
            if re.match(r'[\sOGB]', self.grid[self.y][self.x -
                                                      1]) is not None and re.match(r'[\sOGB]', self.grid[self.y +
                                                                                                         1][self.x -
                                                                                                            1]) is not None and self.x > self.limit_left:
                self.x -= 1
            self.dir = 2
        if dir == 3:
            if re.match(r'[\sOGB]', self.grid[self.y][self.x +
                                                      2]) is not None and re.match(r'[\sOGB]', self.grid[self.y +
                                                                                                         1][self.x +
                                                                                                            2]) is not None and self.x < self.limit_right:
                self.x += 1
            self.dir = 3
        if dir == 4:
            self.y -= 1

        self.put(0)

    def gravity_check(self):
        if re.match(r'[\sEOGSBF8_()]',
                    self.grid[self.y + 2][self.x]) is not None and re.match(r'[\sEOGSFB8_()]',
                                                                            self.grid[self.y + 2][self.x + 1]) is not None:
            self.remove()
            self.y += 1
            self.put(0)
            return 0
        else:
            return 1
