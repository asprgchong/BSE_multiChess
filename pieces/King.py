from Piece import Piece
import pygame

class King(Piece):
    def __init__(self, position, color, board): 
        super(King, self).__init__(pos=position, color=color, board=board)
        if color == "white":
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/wk.png"
        else:
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/bk.png"
