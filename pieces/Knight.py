from Piece import Piece
import pygame

class Knight(Piece):
    def __init__(self, position, color, board): 
        super(Knight, self).__init__(pos=position, color=color, board=board)
        if color == "white":
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/wn.png"
        else:
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/bn.png"
