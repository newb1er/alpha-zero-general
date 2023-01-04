import numpy as np

from Game import Game
from .NoGoLogic import Board

class NoGoGame(Game):
    def __init__(self):
        self.size_x = 9
        self.size_y = 9

    def getInitBoard(self):
        b = Board()
        return np.array(b.grid, np.int32)
    
    def getBoardSize(self):
        return (self.size_x, self.size_y)
    
    def getActionSize(self):
        return (self.size_x * self.size_y) + 1

    def getNextState(self, board, player, action):
        b = Board()
        b.grid = np.copy(board)
        b.execute_move(action, player)
        return (b.grid, -player)

    def getValidMoves(self, board, player):
        valids = [0] * self.getActionSize()
        b = Board()
        b.grid = np.copy(board)
        legalMoves = b.get_legal_moves(player)

        if (len(legalMoves) == 0):
            return np.array(valids)
        
        for action in legalMoves:
            valids[action] = 1
        return np.array(valids)

    def getGameEnded(self, board, player):
        b = Board()
        b.grid = np.copy(board)
        if not b.has_legal_moves(player):
            return -player
        if not b.has_legal_moves(-player):
            return player

        return 0
    
    def getCanonicalForm(self, board, player):
        return player*board
    
    def getSymmetries(self, board, pi):
        # mirror, rotational
        assert(len(pi) == (self.getActionSize()))
        pi_board = np.reshape(pi[:-1], (self.size_x, self.size_y))
        l = []

        for i in range(1, 5):
            for j in [True, False]:
                newB = np.rot90(board, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB = np.fliplr(newB)
                    newPi = np.fliplr(newPi)
                l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l
    
    def stringRepresentation(self, board):
        return board.tostring()
    
    def display(self, board):
        b = Board()
        b.grid = np.copy(board)
        print(b)
        
