import pygame

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

    def get_coord(self):
        columns = 'abcdefgh'
        return columns[self.x] + str(self.y + 1)
    
    def getCurrentOccupyingPiece(self):
        return self.occupying_piece