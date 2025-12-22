import pygame

class Piece():
    def __init__(self, pos, color, board): 
        self.x = pos[0]
        self.y= pos[1]
        self.taken = False
        self.color = color
        self.board = board

    def getPosition(self):
        return (self.x, self.y)

    def getAllValidMoves(self):
        return []