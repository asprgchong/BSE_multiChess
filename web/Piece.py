class Piece():
    def __init__(self, pos, color): 
        self.x = pos[0]
        self.y= pos[1]
        self.taken = False
        self.color = color

    def getPosition(self):
        return (self.x, self.y)
