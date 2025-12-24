import pygame
from pieces.Rook import Rook
from pieces.Knight import Knight
from pieces.Bishop import Bishop
from pieces.Queen import Queen
from pieces.King import King
from pieces.Pawn import Pawn

class Tile: 
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pos = (x, y)
        self.color = 'light' if (x + y) % 2 == 0 else 'dark'
        self.highlight_color = (100, 249, 83) if self.color == 'light' else (0, 228, 10)
        self.occupying_piece = None
        self.coord = self.get_coord()
        self.highlight = False
        # self.rect = pygame.Rect(
        #     self.abs_x,
        #     self.abs_y,
        #     self.width,
        #     self.height
        # )

    def get_coord(self):
        columns = 'abcdefgh'
        return columns[self.x] + str(self.y + 1)
    
    def getCurrentOccupyingPiece(self):
        return self.occupying_piece
    
    def supportingPieces(self, board, check):
        #Maybe this function might be better in the King class.. but I've already implemented it so I can come back and fix it...
        """
        1. To check for pieces that are in the range of the king's legal moves but if these pieces
        are supported, we cannot take with the king. 
            Tile(self) in this case refers to any one of the squares in the king's legal moves set. 
        2. To check if the king is in check at a specific (known) tile because, if there is any piece in the range of the king
        and of opposite color, then we know that the king is in check! 
            Tile(self) refers to the king. 

        Returns a dict of supporting pieces of a piece occupying the specified tile / pieces that are checking the king
        """
        piecesSupporting = {}
        x, y = self.occupying_piece.getPosition()
        color = self.occupying_piece.color
        if check:
            if color == "white":
                color = "black"
            else:
                color = "white"
        print(color)
        #pawn check
        pawnUnit = [(0, 1), (-1,1), (1,1)]
        if color == "black":
            pawnUnit = [(k[0] * -1, k[1]*-1)for k in pawnUnit]

        for eachdir in pawnUnit:
            if (x + eachdir[0] <= 7 and x + eachdir[0] >= 0) and (y+eachdir[1] <= 7 and y+eachdir[1] >= 0):
                piece = board.config[y+eachdir[1]][x+eachdir[0]].getCurrentOccupyingPiece()
                #checks if there is a piece there
                if piece is not None and isinstance(piece, Pawn) and piece.color == color:
                    #check if the piece is an supp pawn 
                    piecesSupporting[(x + eachdir[0], y+eachdir[1])] = piece
                    #add the position of that supp pawn to list

        #note that the check of a bishop and rook together negates a Queen! 
        #bishops check
        for i in range(1,x+1): #cells to the left
            if (x + (i * -1) >= 0) and (y - (i*1) <= 7 and y - (i*1) >= 0):
                piece = board.config[y - (i * 1)][x + (i * -1)].getCurrentOccupyingPiece()
                if piece is not None and (isinstance(piece, Bishop) or isinstance(piece, Queen)) and piece.color == color:
                    piecesSupporting[(x + (i * -1),y - (i * 1))] = piece
                    break
        for i in range(1,x+1):
            if (x + (i * -1) >= 0) and (y + (i*1) <= 7):
                #going to the top left diag of piece  
                piece = board.config[y + (i * 1)][x + (i * -1)].getCurrentOccupyingPiece()
                if piece is not None and (isinstance(piece, Bishop) or isinstance(piece, Queen)) and piece.color == color:
                    piecesSupporting[(x + (i * -1),y + (i * 1))] = piece
                    break
            
        for i in range(1, 7-x):
            if (x + (i * 1) <= 7) and (y - (i*1) >= 0):
                #going to the top right diag of piece
                piece = board.config[y - (i * 1)][x + (i * 1)].getCurrentOccupyingPiece()
                if piece is not None and (isinstance(piece, Bishop) or isinstance(piece, Queen)) and piece.color == color:
                    piecesSupporting[(x + (i * 1),y - (i * 1))] = piece
                    break

        for i in range(1, 7-x):
            if (x + (i * 1) <= 7) and (y + (i*1) <= 7):
                #going to the bottom right diag of piece
                piece = board.config[y + (i * 1)][x + (i * 1)].getCurrentOccupyingPiece()
                if piece is not None and (isinstance(piece, Bishop) or isinstance(piece, Queen)) and piece.color == color:
                    piecesSupporting[(x + (i * 1),y + (i * 1))] = piece
                    break

        #rook check
        for i in range(x-1, -1, -1):
            piece = board.config[y][i].getCurrentOccupyingPiece()
            if piece is not None and (isinstance(piece, Rook) or isinstance(piece, Queen)) and piece.color == color:
                piecesSupporting[(i,y)] = piece
                break

        for i in range(x+1, 8):
            piece = board.config[y][i].getCurrentOccupyingPiece()
            if piece is not None and (isinstance(piece, Rook) or isinstance(piece, Queen)) and piece.color == color:
                piecesSupporting[(i,y)] = piece
                break


        for j in range(y-1, -1, -1):
            piece = board.config[j][x].getCurrentOccupyingPiece()
            if piece is not None and (isinstance(piece, Rook) or isinstance(piece, Queen)) and piece.color == color:
                piecesSupporting[(x,j)] = piece
                break

        for j in range(y+1, 8):
            piece = board.config[j][x].getCurrentOccupyingPiece()
            if piece is not None and (isinstance(piece, Rook) or isinstance(piece, Queen)) and piece.color == color:
                piecesSupporting[(x,j)] = piece
                break

        return piecesSupporting