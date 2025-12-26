from Piece import Piece

class Queen(Piece):
    def __init__(self, position, color): 
        super(Queen, self).__init__(pos=position, color=color)
        self.image = f"assets/{'wq' if color == 'white' else 'bq'}.png"

    def get_legal_moves(self, board):
        moves = []
        x, y = self.getPosition()
        unitDirections = [(0,1), (0,-1), (1,0), (-1,0), (1,1), (1,-1), (-1,1), (-1,-1)]

        for dx, dy in unitDirections:
            for i in range(1, 8):
                nx, ny = x + (dx * i), y + (dy * i)
                if 0 <= nx < 8 and 0 <= ny < 8:
                    target = board.config[ny][nx].getCurrentOccupyingPiece()
                    if target is None:
                        moves.append((nx, ny))
                    elif target.color != self.color:
                        moves.append((nx, ny))
                        break
                    else:
                        break
                else:
                    break
        return moves