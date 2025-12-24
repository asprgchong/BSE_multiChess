from Piece import Piece

class Pawn(Piece):
    def __init__(self, position, color, board): 
        super(Pawn, self).__init__(pos=position, color=color, board=board)
        self.image = f"assets/{'wp' if color == 'white' else 'bp'}.png"
        self.doubleUp = (True, 0)
        self.enpassant = False

    def get_legal_moves(self, board):
        legal_moves = []
        x, y = self.getPosition()

        unitDirections = [(0,1), (1,1), (-1,1)]

        if self.doubleUp[0]:
            unitDirections.append((0,2))
        
        if self.color == "white":
            unitDirections = [(dx * -1, dy * -1) for dx, dy in unitDirections]

        for eachdir in unitDirections:
            nx, ny = x + eachdir[0], y + eachdir[1]
            if 0 <= nx < 8 and 0 <= ny < 8:
                piece = board.config[ny][nx].getCurrentOccupyingPiece()
                if piece is not None:
                    # Can only capture diagonally
                    if piece.color != self.color and eachdir[0] != 0:
                        legal_moves.append((nx, ny))
                else:
                    # Can only move forward to empty squares
                    if eachdir[0] == 0:
                        legal_moves.append((nx, ny))

        return legal_moves