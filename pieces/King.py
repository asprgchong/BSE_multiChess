from Piece import Piece

class King(Piece):
    def __init__(self, position, color, board): 
        super(King, self).__init__(pos=position, color=color, board=board)
        self.image = f"assets/{'wk' if color == 'white' else 'bk'}.png"

    def get_legal_moves(self, board):
        moves = []
        x, y = self.getPosition()
        unitDirections = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]

        for dx, dy in unitDirections:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board.config[ny][nx].getCurrentOccupyingPiece()
                if target is None or target.color != self.color:
                    moves.append((nx, ny))
        return moves