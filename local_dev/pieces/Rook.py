from Piece import Piece

class Rook(Piece):
    def __init__(self, position, color):
        super(Rook, self).__init__(position, color)
        self.image = f"assets/{'wr' if color == 'white' else 'br'}.png"

    def get_legal_moves(self, board):
        legal_moves = []
        x, y = self.getPosition()

        for i in range(x-1, -1, -1):
            piece = board.config[y][i].getCurrentOccupyingPiece()
            if piece is not None:
                if piece.color != self.color:
                    legal_moves.append((i, y))
                break
            legal_moves.append((i, y))
            
        for i in range(x+1, 8):
            piece = board.config[y][i].getCurrentOccupyingPiece()
            if piece is not None:
                if piece.color != self.color:
                    legal_moves.append((i, y))
                break
            legal_moves.append((i, y))

        for j in range(y-1, -1, -1):
            piece = board.config[j][x].getCurrentOccupyingPiece()
            if piece is not None:
                if piece.color != self.color:
                    legal_moves.append((x, j))
                break
            legal_moves.append((x, j))

        for j in range(y+1, 8):
            piece = board.config[j][x].getCurrentOccupyingPiece()
            if piece is not None:
                if piece.color != self.color:
                    legal_moves.append((x, j))
                break
            legal_moves.append((x, j))

        return legal_moves