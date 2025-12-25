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
        self.blackKing = None
        self.whiteKing = None 
        self.whiteenpassants = []
        self.blackenpassants = []

    def boardSetUp(self):
        result = []
        for rowindex, eachrow in enumerate(self.config):
            row = [] 
            for index, eachTile in enumerate(eachrow):
                if eachTile == '':
                    newTile = Tile(index, rowindex, cellwidth, cellwidth)
                    row.append(newTile)
                    continue
                    
                # make the piece and place on corresponding tile
                if "b" in eachTile:
                    color = "black"
                else: 
                    color = "white"

                if "R" in eachTile:
                    newPiece = Rook((index, rowindex), color, self)
                elif "N" in eachTile: 
                    newPiece = Knight((index, rowindex), color, self)
                elif "B" in eachTile:
                    newPiece = Bishop((index, rowindex), color, self)
                elif "Q" in eachTile:
                    newPiece = Queen((index, rowindex), color, self)
                elif "K" in eachTile:
                    newPiece = King((index, rowindex), color, self)
                    if color == "white":
                        self.whiteKing = (index, rowindex)
                    else:
                        self.blackKing = (index, rowindex)
                elif "P" in eachTile:
                    newPiece = Pawn((index, rowindex), color, self)

                newTile = Tile(newPiece.x, newPiece.y, cellwidth, cellwidth)
                newTile.occupying_piece = newPiece
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
                pygame.draw.rect(screen, pygame.Color(199, 199, 199,1), (
                    (((column * (cellwidth*2))+cellwidth)+leftPush, (row * cellwidth)+topPush, cellwidth, cellwidth
                )))
            else: 
                pygame.draw.rect(screen, pygame.Color(199, 199, 199,1), (
                    (column * (cellwidth*2))+leftPush, (row * cellwidth)+topPush, cellwidth, cellwidth
                ))
                pygame.draw.rect(screen, pygame.Color(105, 105, 105,1), (
                    (((column * (cellwidth*2))+cellwidth)+leftPush, (row * cellwidth)+topPush, cellwidth, cellwidth
                )))  
        
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
                    self.pieceMapping.append((piece, 1))

                    screen.blit(piece_scaled, piece_rect)

    def is_square_attacked(self, x, y, by_color):
        for row in self.config:
            for tile in row:
                piece = tile.getCurrentOccupyingPiece()
                if piece and piece.color == by_color:
                    if isinstance(piece, King):
                        px, py = piece.getPosition()
                        if abs(px - x) <= 1 and abs(py - y) <= 1 and (px != x or py != y):
                            return True
                    elif isinstance(piece, Pawn):
                        px, py = piece.getPosition()
                        direction = -1 if piece.color == "white" else 1
                        if py + direction == y and abs(px - x) == 1:
                            return True
                    else:
                        moves = piece.get_legal_moves(self)
                        if (x, y) in moves:
                            return True
        return False

    def would_be_in_check(self, piece, new_x, new_y):
        old_x, old_y = piece.getPosition()
        captured_piece = self.config[new_y][new_x].getCurrentOccupyingPiece()
        
        self.config[old_y][old_x].occupying_piece = None
        self.config[new_y][new_x].occupying_piece = piece
        piece.x = new_x
        piece.y = new_y
        
        if piece.color == "white":
            king_pos = self.whiteKing if not isinstance(piece, King) else (new_x, new_y)
        else:
            king_pos = self.blackKing if not isinstance(piece, King) else (new_x, new_y)
        
        opponent_color = "black" if piece.color == "white" else "white"
        in_check = self.is_square_attacked(king_pos[0], king_pos[1], opponent_color)
        
        piece.x = old_x
        piece.y = old_y
        self.config[old_y][old_x].occupying_piece = piece
        self.config[new_y][new_x].occupying_piece = captured_piece
        
        return in_check

    def get_legal_moves_for_piece(self, piece):
        """
            Get all legal moves for a piece, filtering out moves that would leave king in check
        """
        pseudo_legal_moves = piece.get_legal_moves(self)
        legal_moves = []
        
        for move in pseudo_legal_moves:
            if not self.would_be_in_check(piece, move[0], move[1]):
                legal_moves.append(move)
        
        return legal_moves

    def getPieceAtCoord(self, x, y):
        if self.config[y][x].getCurrentOccupyingPiece() is None:
            return "No pieces here!"
        piece = self.config[y][x].getCurrentOccupyingPiece()
        if isinstance(piece, Pawn):
            return "Pawn"
        elif isinstance(piece, Rook):
            return "Rook"
        elif isinstance(piece, Knight):
            return "Knight"
        elif isinstance(piece, Bishop):
            return "Bishop"
        elif isinstance(piece, King):
            return "King"
        elif isinstance(piece, Queen):
            return "Queen"
        
    def updateConfig(self, index, prevPosition, capture=False):
        piece = self.pieceMapping[index][0]
        if isinstance(piece, Pawn):
            if piece.doubleUp[0] and abs(piece.y - prevPosition[1]) == 2:
                piece.doubleUp = (False, 1)
                if piece.color == "white":
                    self.whiteenpassants.append(piece)
                else:
                    self.blackenpassants.append(piece) 
            else: 
                piece.doubleUp = (piece.doubleUp[0], piece.doubleUp[1] + 1)
        elif isinstance(piece, King):
            if piece.color == "white":
                self.whiteKing = (piece.x, piece.y)
            else:
                self.blackKing = (piece.x, piece.y)

        if capture:
            self.config[prevPosition[1]][prevPosition[0]].occupying_piece = None
            self.pieceMapping[index] = (piece, 0)
        else:
            self.config[piece.y][piece.x].occupying_piece = piece
            self.config[prevPosition[1]][prevPosition[0]].occupying_piece = None

        if piece.color == "white":
            self.blackenpassants = []
        else:
            self.whiteenpassants = []

    def is_in_check(self, color):
        """
        Check if the king of the given color is in check

        """
        king_pos = self.whiteKing if color == "white" else self.blackKing
        opponent_color = "black" if color == "white" else "white"
        return self.is_square_attacked(king_pos[0], king_pos[1], opponent_color)

    def checkmate(self, turn):
        next_color = "black" if turn == "white" else "white"
      
        has_legal_move = False
        for row in self.config:
            for tile in row:
                piece = tile.getCurrentOccupyingPiece()
                if piece and piece.color == next_color:
                    if self.get_legal_moves_for_piece(piece):
                        has_legal_move = True
                        break
            if has_legal_move:
                break
        
        if not has_legal_move:
            if self.is_in_check(next_color):
                return "checkmate"
            else:
                return "stalemate"
        
        return "nope"