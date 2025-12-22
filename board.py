from tile import Tile
from pieces.Rook import Rook
from pieces.Knight import Knight
from pieces.Bishop import Bishop
from pieces.Queen import Queen
from pieces.King import King
from pieces.Pawn import Pawn
import pygame

cellwidth = 120
leftPush = 40
topPush = 30

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tile_width = width // 8
        self.tile_height = height // 8
        self.selected_piece = None
        self.turn = 'white'
        self.config = [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
        self.activePieces = []

    # def displayCurrentBoard(self):
    #     for row in self.config:
    #         for eachTile in row: 
    #             piece = eachTile.getCurrentOccupyingPiece()
    #             if piece is not None: 
    #                 # print((piece.x,piece.y), end="")
    #                 print(piece, end="")
    #                 print(" | ", end="")
    #             else: 
    #                 print('',end="")
    #                 print(" | ", end="")
    #         print("")

    def boardSetUp(self):
        result = []
        pieces = [] 
        for rowindex, eachrow in enumerate(self.config):
            row = [] 
            for index, eachTile in enumerate(eachrow):
                # make the piece and place on corresponding tile
                if "b" in eachTile:
                    color = "black"
                else: 
                    color = "white"

                # leftAdd = (cellwidth) * (color == "black") * index
                # topAdd = (cellwidth) * rowindex
                if "R" in eachTile:
                    newPiece = Rook((index, rowindex), color, self)
                elif "N" in eachTile: 
                    newPiece = Knight((index, rowindex), color, self)
                elif "B" in eachTile:
                    newPiece = Bishop((index, rowindex), color, self)
                elif "Q" in eachTile:
                    newPiece = Queen((index, rowindex), color,self)
                elif "K" in eachTile:
                    newPiece = King((index, rowindex), color,self)
                elif "P" in eachTile:
                    newPiece = Pawn((index, rowindex), color, self)

                newTile = Tile(newPiece.x, newPiece.y, cellwidth, cellwidth)
                if eachTile != '':
                    newTile.occupying_piece = newPiece
                    pieces.append(newPiece)
                row.append(newTile)
            result.append(row)
        self.config = result
        self.activePieces = pieces

    def draw_board(self, screen):
        for i in range(32):
            column = i % 4
            row = i // 4
            if row % 2 != 0: 
                pygame.draw.rect(screen, pygame.Color(105, 105, 105,1), (
                    (column * (cellwidth*2))+leftPush, (row * cellwidth)+topPush, cellwidth, cellwidth
                ))
                #left coord, top coord, width, height
                pygame.draw.rect(screen, pygame.Color(199, 199, 199,1), (
                    (((column * (cellwidth*2))+cellwidth)+leftPush, (row * cellwidth)+topPush, cellwidth, cellwidth
                )))
            else: 
                pygame.draw.rect(screen, pygame.Color(199, 199, 199,1), (
                    (column * (cellwidth*2))+leftPush, (row * cellwidth)+topPush, cellwidth, cellwidth
                ))
                #left coord, top coord, width, height
                pygame.draw.rect(screen, pygame.Color(105, 105, 105,1), (
                    (((column * (cellwidth*2))+cellwidth)+leftPush, (row * cellwidth)+topPush, cellwidth, cellwidth
                )))  

    def draw_pieces(self, screen):
        ## Puts every piece on the board
        for rindex, row in enumerate(self.config):
            for index, tile in enumerate(row):
                piece = tile.getCurrentOccupyingPiece()
                if piece is not None:
                    image = pygame.image.load(piece.image)
                    piece_scaled = pygame.transform.scale(image, (100, 100))
                    screen.blit(piece_scaled, ((index * cellwidth) + (leftPush * 1.2), (rindex * cellwidth) + (topPush * 1.2)))

# Might need a set of 