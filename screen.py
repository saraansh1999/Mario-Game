import re


class Screen():

    def __init__(self, dimensions):
        self.grid = []
        self.width = dimensions[0]
        self.height = dimensions[1]

    def make_grid(self):
        for j in range(0, self.height):
            self.grid.append([])
            for i in range(0, self.width):
                if i == 0 or i == self.width - 1 or j < 2 or j > self.height - 5:
                    self.grid[j].append('X')
                else:
                    self.grid[j].append(' ')

    def blit(self, start, end):
        print('\033[1m')
        for i in range(0, self.height):
            for j in range(start, end):
                if self.grid[i][j] == 'O' or self.grid[i][j] == 'G':
                    print('\033[93m' + self.grid[i][j] + '\033[97m', end='')
                elif self.grid[i][j] == 'M' or self.grid[i][j] == 'L':
                    print('\033[32m' + self.grid[i][j] + '\033[97m', end='')
                elif self.grid[i][j] == 'E' or self.grid[i][j] == 'B' or self.grid[i][j] == 'F' or self.grid[i][j] == 'S':
                    print('\033[31m' + self.grid[i][j] + '\033[97m', end='')
                else:
                    print(self.grid[i][j], end='')
            print('')
        print('\033[0m')
