from Piece import Piece
import pygame

class Knight(Piece):
    def __init__(self, position, color, board): 
        super(Knight, self).__init__(pos=position, color=color, board=board)
        if color == "white":
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/wn.png"
        else:
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/bn.png"

    def get_legal_moves(self, board):
        legal_moves = []
        x, y = self.getPosition()

        unitDirections = [(-1,2), (1,2), (-2,1), (2,1), (-2,-1), (2, -1), (-1,-2), (1,-2)]
        for eachdir in unitDirections:
            if (x+eachdir[0] <= 7 and x+eachdir[0] >= 0) and (y+eachdir[1] <= 7 and y+eachdir[1] >= 0):
                piece = board.config[y+eachdir[1]][x+eachdir[0]].getCurrentOccupyingPiece()
                if piece is not None:
                    if piece.color != self.color:
                        legal_moves.append((x+eachdir[0], y+eachdir[1]))
                else:
                    legal_moves.append((x+eachdir[0], y+eachdir[1]))

        return legal_moves