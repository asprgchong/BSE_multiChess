from Piece import Piece
import pygame

class Pawn(Piece):
    def __init__(self, position, color, board): 
        super(Pawn, self).__init__(pos=position, color=color, board=board)
        if color == "white":
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/wp.png"
        else:
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/bp.png"
        self.doubleUp = (True, 0)
        self.enpassant = False

    def get_legal_moves(self, board):
        legal_moves = []
        x, y = self.getPosition()

        unitDirections = [(0,1), (1,1), (-1,1)]

        if self.doubleUp[0]:
            unitDirections.append((0,2))
        
        '''
        check if en passant is available:
        Need to have moved 3 ranks to qualify
        Check if there is opponent pawn next to self
        Check if that opponent pawn has just been updated to doubleUp
        '''
        if (self.color == "black" and y >= 3) or (self.color == "white" and y <= 4):
            opppieceRight = board.config[y][x+1].getCurrentOccupyingPiece()
            opppieceLeft = board.config[y][x-1].getCurrentOccupyingPiece()
            if opppieceRight is not None and (isinstance(opppieceRight,Pawn) and opppieceRight.doubleUp == (False, 1)):
                legal_moves.append((-1, 1))
                self.enpassant = True
            if opppieceLeft is not None and (isinstance(opppieceRight,Pawn) and opppieceLeft.doubleUp == (False, 1)):
                legal_moves.append((1, 1))
                self.enpassant = True
        
        if self.color == "white":
            unitDirections = [(x[0] * -1, x[1]*-1) for x in unitDirections]

        for eachdir in unitDirections:
            if (x+eachdir[0] <= 7 and x+eachdir[0] >= 0) and (y+eachdir[1] <= 7 and y+eachdir[1] >= 0):
                piece = board.config[y+eachdir[1]][x+eachdir[0]].getCurrentOccupyingPiece()
                if piece is not None:
                    if piece.color != self.color:
                        legal_moves.append((x+eachdir[0], y+eachdir[1]))
                else:
                    if eachdir[0] == 0:
                        legal_moves.append((x+eachdir[0], y+eachdir[1]))
        return legal_moves        
        