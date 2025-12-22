from Piece import Piece
import pygame

class Rook(Piece):
    def __init__(self, position, color,board):
        super(Rook, self).__init__(position, color,board)
        if color == "white":
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/wr.png"
        else:
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/br.png"