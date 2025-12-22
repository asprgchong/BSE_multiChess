from Piece import Piece
import pygame

class Bishop(Piece):
    def __init__(self, position, color, board): 
        super(Bishop, self).__init__(pos=position, color=color, board=board)
        if color == "white":
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/wb.png"
        else:
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/bb.png"
