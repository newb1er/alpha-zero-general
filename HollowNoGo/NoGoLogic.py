from enum import Enum
import numpy as np

class Piece(Enum):
    EMPTY = 0
    BLACK = 1
    WHITE = -1
    HOLE = 3
    UNKNOWN = 4

class Board():
    def __init__(self):
        self.size_x = 9
        self.size_y = 9
        self.grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 3, 0, 0, 0, 0],
                     [0, 0, 0, 0, 3, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 3, 3, 0, 0, 0, 3, 3, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 3, 0, 0, 0, 0],
                     [0, 0, 0, 0, 3, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # self.grid = [[0 for x in range(self.size_x)] for y in range(self.size_y)]
        # self.grid[4][1] = Piece.HOLE.value
        # self.grid[4][2] = Piece.HOLE.value
        # self.grid[4][6] = Piece.HOLE.value
        # self.grid[4][7] = Piece.HOLE.value
        # self.grid[1][4] = Piece.HOLE.value
        # self.grid[2][4] = Piece.HOLE.value
        # self.grid[6][4] = Piece.HOLE.value
        # self.grid[7][4] = Piece.HOLE.value

    def __getitem__(self, index):
        return self.grid[index]

    def execute_move(self, action, player):
        x = action % self.size_x
        y = action // self.size_y
        self.grid[x][y] = player
    
    def check_liberty(self, x, y, player):
        test = np.copy(self.grid)
        if x < 0 or x >= self.size_x:
            return False
        if y < 0 or y >= self.size_y:
            return False
        
        queue = [(x, y)]
        liberty = False

        for x, y in queue:
            test[x][y] = Piece.UNKNOWN.value
            if x > 0:
                if test[x-1][y] == Piece.EMPTY.value:
                    liberty = True
                    break
                elif test[x-1][y] == player:
                    queue.append((x-1, y))
            
            if x < self.size_x - 1:
                if test[x+1][y] == Piece.EMPTY.value:
                    liberty = True
                    break
                elif test[x+1][y] == player:
                    queue.append((x+1, y))
            
            if y > 0:
                if test[x][y-1] == Piece.EMPTY.value:
                    liberty = True
                    break
                elif test[x][y-1] == player:
                    queue.append((x, y-1))
            
            if y < self.size_y - 1:
                if test[x][y+1] == Piece.EMPTY.value:
                    liberty = True
                    break
                elif test[x][y+1] == player:
                    queue.append((x, y+1))

        return liberty
    
    def check_legal_move(self, action, player):
        x = action % self.size_x
        y = action // self.size_y
        if x < 0 or x >= self.size_x:
            return False       
        if y < 0 or y >= self.size_y:
            return False

        if abs(self.grid[x][y]) == Piece.HOLE.value:
            return False
        
        if self.grid[x][y] != Piece.EMPTY.value:
            return False
        
        self.grid[x][y] = player

        if not self.check_liberty(x, y, player):
            self.grid[x][y] = Piece.EMPTY.value
            return False
        if x > 0 and not self.check_liberty(x-1, y, -player):
            self.grid[x][y] = Piece.EMPTY.value
            return False
        if x < self.size_x - 1 and not self.check_liberty(x+1, y, -player):
            self.grid[x][y] = Piece.EMPTY.value
            return False
        if y > 0 and not self.check_liberty(x, y-1, -player):
            self.grid[x][y] = Piece.EMPTY.value
            return False
        if y < self.size_y - 1 and not self.check_liberty(x, y+1, -player):
            self.grid[x][y] = Piece.EMPTY.value
            return False
        
        self.grid[x][y] = Piece.EMPTY.value

        return True
    
    def has_legal_moves(self, player):
        for action in range(self.size_x * self.size_y):
            if self.check_legal_move(action, player):
                return True
        return False

    def get_legal_moves(self, player):
        l = []
        for action in range(self.size_x * self.size_y):
            if self.check_legal_move(action, player):
                l.append(action)
        
        return l
        
    def __str__(self):
        s = ""
        for y in range(self.size_y):
            for x in range(self.size_x):
                if self.grid[x][y] == Piece.EMPTY.value:
                    s += "\u00B7 "
                elif self.grid[x][y] == Piece.BLACK.value:
                    s += "\u25CF "
                elif self.grid[x][y] == Piece.WHITE.value:
                    s += "\u25CB "
                elif self.grid[x][y] == Piece.HOLE.value:
                    s += "  "
                else:
                    s += "  "
            s += "\n"
        
        return s