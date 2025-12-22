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
        self.pieceMapping = []

    def displayCurrentBoard(self):
        for row in self.config:
            for eachTile in row: 
                piece = eachTile.getCurrentOccupyingPiece()
                if piece is not None: 
                    print((piece.x,piece.y, self.getPieceAtCoord(piece.x, piece.y)), end="")
                    print(" | ", end="")
                else: 
                    print('',end="")
                    print(" | ", end="")
            print("")

    def boardSetUp(self):
        result = []
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
                # print(index, rowindex, eachTile)
                row.append(newTile)
            result.append(row)
        self.config = result

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
        
        #Adding the indexes to each column and row
        for i in range(8):
            font = pygame.font.Font(None, 36)
            text = font.render(str(i), False, (255, 255, 255))
            screen.blit(text, ((leftPush + 5) + ((i) * cellwidth), (topPush + 5)))
        for i in range(8):
            font = pygame.font.Font(None, 36)
            text = font.render(str(i), False, (255, 255, 255))
            screen.blit(text, ((leftPush + 5), (topPush + 5)+ ((i) * cellwidth)))

    def draw_pieces(self, screen):
        self.activePieces = []
        self.pieceMapping = []
        
        for row in self.config:
            for tile in row:
                piece = tile.getCurrentOccupyingPiece()
                if piece is not None:
                    image = pygame.image.load(piece.image).convert_alpha()
                    piece_scaled = pygame.transform.scale(image, (100, 100))
                    piece_rect = piece_scaled.get_rect(topleft=((piece.x * cellwidth) + (leftPush * 1.2), (piece.y * cellwidth) + (topPush * 1.2)))
                    self.activePieces.append(piece_rect)
                    self.pieceMapping.append(piece)

                    screen.blit(piece_scaled, piece_rect)

    def getPieceAtCoord(self, x ,y):
        if self.config[y][x].getCurrentOccupyingPiece() is None:
            return "No pieces here!"
        elif isinstance(self.config[y][x].getCurrentOccupyingPiece(),Pawn):
            return "Pawn"
        elif isinstance(self.config[y][x].getCurrentOccupyingPiece(), Rook):
            return "Rook"
        elif isinstance(self.config[y][x].getCurrentOccupyingPiece(), Knight):
            return "Knight"
        elif isinstance(self.config[y][x].getCurrentOccupyingPiece(), Bishop):
            return "Bishop"
        elif isinstance(self.config[y][x].getCurrentOccupyingPiece(), King):
            return "King"
        elif isinstance(self.config[y][x].getCurrentOccupyingPiece(), Queen):
            return "Queen"
        
    def updateConfig(self, index, prevPosition):
        if index is not None:
            piece = self.pieceMapping[index]
            self.config[piece.y][piece.x].occupying_piece = piece
            self.config[prevPosition[1]][prevPosition[0]].occupying_piece = None
        else:
            self.config[prevPosition[1]][prevPosition[0]].occupying_piece = None
            