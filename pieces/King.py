from Piece import Piece
from pieces.Rook import Rook

class King(Piece):
    def __init__(self, position, color, board): 
        super(King, self).__init__(pos=position, color=color, board=board)
        self.image = f"assets/{'wk' if color == 'white' else 'bk'}.png"
        self.castle = True

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

        castle = {
                    "king": [((1, 0), None), ((2,0), None), ((3,0), "Rook")],
                    "queen": [((-1, 0), None), ((-2,0), None), ((-3,0), None), ((-4, 0), "Rook")]
                }
        
        if self.castle:
            king = True
            queen = True
            for key, type in castle.items():
                for each in type:
                    pos, occ = each
                    if occ == "Rook":  
                        if not isinstance(board.config[self.y + pos[1]][self.x + pos[0]].getCurrentOccupyingPiece(), Rook):
                            if key == "king":
                                king = False
                            if key == "queen":
                                queen = False
                            break
                    else:
                        if board.config[self.y + pos[1]][self.x + pos[0]].getCurrentOccupyingPiece() is not None:
                            if key == "king":
                                king = False
                            if key == "queen":
                                queen = False
                            break
            if king:
                moves.append((self.x + 2, self.y))
            if queen:
                moves.append((self.x - 2, self.y))
            print("Castle king side? ", king)
            print("Castle queen side ", queen)
            
        return moves