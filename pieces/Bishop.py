from Piece import Piece
import pygame

class Bishop(Piece):
    def __init__(self, position, color, board): 
        super(Bishop, self).__init__(pos=position, color=color, board=board)
        if color == "white":
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/wb.png"
        else:
            self.image = "/home/geralyn/Documents/buildEveryday/multiChessPlayer/assets/bb.png"

    def get_legal_moves(self, board): 
        legal_moves = []
        x,y = self.getPosition()

        for i in range(1,x+1): #cells to the left
            if (x + (i * -1) >= 0) and (y - (i*1) <= 7 and y - (i*1) >= 0):
                #going to the bottom left diag of piece
                piece = board.config[y - (i * 1)][x + (i * -1)].getCurrentOccupyingPiece()
                if piece is not None:
                    if piece.color != self.color:
                        legal_moves.append((x + (i * -1), y - (i * 1)))
                    break
                legal_moves.append((x + (i * -1), y - (i * 1)))

        for i in range(1,x+1):
            if (x + (i * -1) >= 0) and (y + (i*1) <= 7):
                #going to the top left diag of piece  
                piece = board.config[y + (i * 1)][x + (i * -1)].getCurrentOccupyingPiece()
                if piece is not None:
                    if piece.color != self.color:
                        legal_moves.append((x + (i * -1), y + (i * 1)))
                    break
                legal_moves.append((x + (i * -1), y + (i * 1)))
            
            
        for i in range(1, 7-x):
            if (x + (i * 1) <= 7) and (y - (i*1) >= 0):
                #going to the top right diag of piece
                piece = board.config[y - (i * 1)][x + (i * 1)].getCurrentOccupyingPiece()
                if piece is not None:
                    if piece.color != self.color:
                        legal_moves.append((x + (i * 1), y - (i * 1)))
                    break
                legal_moves.append((x + (i * 1), y - (i * 1)))

        for i in range(1, 7-x):
            if (x + (i * 1) <= 7) and (y + (i*1) <= 7):
                #going to the bottom right diag of piece
                piece = board.config[y + (i * 1)][x + (i * 1)].getCurrentOccupyingPiece()
                if piece is not None:
                    if piece.color != self.color:
                        legal_moves.append((x + (i * 1), y + (i * 1)))
                    break
                legal_moves.append((x + (i * 1), y + (i * 1)))
        
        return legal_moves