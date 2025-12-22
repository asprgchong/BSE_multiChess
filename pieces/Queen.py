from Piece import Piece
import pygame

class Queen(Piece):
    def __init__(self, position, color, board): 
        super(Queen, self).__init__(pos=position, color=color, board=board)
        if color == "white":
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/wq.png"
        else:
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/bq.png"

    def allPossibleMoves(self):
        #Given the current position of the piece, we want to calculate all the possible moves it could make
        return []