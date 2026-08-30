from board import Board
from Piece import Piece
from pieces import Pawn
import pytest

@pytest.fixture
def setup_Board():
    board = Board(960, 960)
    board.boardSetUp()
    return board

@pytest.fixture
def setup_Board_e4_d5():
    board = Board(960, 960)
    board.boardSetUp()

    whitePawn = board.config[6][4].occupying_piece
    board.config[6][4].occupying_piece = None
    board.config[4][4].occupying_piece = whitePawn
    whitePawn.x, whitePawn.y = 4, 4

    black_pawn = board.config[1][3].occupying_piece
    board.config[1][3].occupying_piece = None
    board.config[3][3].occupying_piece = black_pawn
    black_pawn.x, black_pawn.y = 3, 3

    board.turn = "white"
    return board


def test_pawn_moves_two_on_first_move(setup_Board):
    board = setup_Board
    pawn = board.config[6][4].getCurrentOccupyingPiece()
    moves = board.get_legal_moves_for_piece(pawn)
    assert (4, 4) in moves

def test_pawn_move_one(setup_Board):
    board = setup_Board
    pawn = board.config[6][5].getCurrentOccupyingPiece()
    assert (5, 5) in board.get_legal_moves_for_piece(pawn)

def test_pawn_capture_e4d5(setup_Board_e4_d5):
    board = setup_Board_e4_d5
    white_pawn = board.config[4][4].occupying_piece
    legal_moves = board.get_legal_moves_for_piece(white_pawn)
    assert (3, 3) in legal_moves