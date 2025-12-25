from Piece import Piece

class Pawn(Piece):
    def __init__(self, position, color, board): 
        super(Pawn, self).__init__(pos=position, color=color, board=board)
        self.image = f"assets/{'wp' if color == 'white' else 'bp'}.png"
        self.doubleUp = (True, 0)

    def get_legal_moves(self, board):
        legal_moves = []
        x, y = self.getPosition()

        unitDirections = [(0,1), (1,1), (-1,1)]

        if self.doubleUp[0]:
            unitDirections.append((0,2))

        if self.color == "white":
            enpassants = board.blackenpassants
        else:
            enpassants = board.whiteenpassants

        if enpassants != []:
            # Check if pawn (self) has moved at least 3 ranks 
            # and there is an opponent pawn in enpassants that is of the same rank and either right or left of self
            if (self.y <= 3 and self.color == "white") or (self.y >= 4 and self.color == "black"):
                if self.x + 1 <= 7: 
                    pr = board.config[self.y][self.x+1].getCurrentOccupyingPiece()
                    if pr is not None and isinstance(pr, Pawn) and (pr.color != self.color) and (pr in enpassants):
                        if self.color == "white":
                            legal_moves.append((pr.x, self.y - 1))
                        else:
                            legal_moves.append((pr.x, self.y + 1))
                if self.x - 1 >= 0:
                    pl = board.config[self.y][self.x-1].getCurrentOccupyingPiece()
                    if pl is not None and isinstance(pl, Pawn) and (pl.color != self.color) and (pl in enpassants):
                        if self.color == "white":
                            legal_moves.append((pl.x, self.y - 1))
                        else:
                            legal_moves.append((pl.x, self.y + 1))
                
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
