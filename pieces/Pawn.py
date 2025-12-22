from Piece import Piece
import pygame

class Pawn(Piece):
    def __init__(self, position, color, board): 
        super(Pawn, self).__init__(pos=position, color=color, board=board)
        if color == "white":
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/wp.png"
        else:
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/bp.png"
