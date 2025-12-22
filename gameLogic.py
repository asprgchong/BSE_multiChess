from board import Board    
import pygame
import sys

WIDTH = 1500
HEIGHT = 1200

pygame.init()
screen = pygame.display.set_caption("Today's Puzzle")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
cellwidth = 120
leftPush = 40
topPush = 30

running = True
board = Board(960, 960)
board.boardSetUp()
# print(board.getPieceAtCoord(7,5))
# board.displayCurrentBoard()
active_box = None
dragging = False
prevMove = None
currPieceLegalMoves = []
turn = "white"

while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i, eachPiece in enumerate(board.activePieces):
                    if eachPiece.collidepoint(event.pos):
                        active_box = i 
                        currPieceLegalMoves = board.pieceMapping[active_box].get_legal_moves(board)
                        prevMove = board.pieceMapping[active_box].getPosition()
                        dragging = True
        if event.type == pygame.MOUSEMOTION:
            if active_box is not None:
                piece = board.pieceMapping[active_box]
                piece.x = (event.pos[0] - leftPush) // cellwidth
                piece.y = (event.pos[1] - topPush) // cellwidth
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                piece = board.pieceMapping[active_box]
                if board.pieceMapping[active_box].color == turn:
                    if piece.getPosition() in currPieceLegalMoves:
                        #ensures that we are only moving to the correct squares 
                        if prevMove is not None and (piece.x != prevMove[0] or piece.y != prevMove[1]):
                            #check if we are taking a piece
                            oppPiece = board.config[piece.y][piece.x].getCurrentOccupyingPiece()
                            if oppPiece is not None:
                                #we are taking a piece here so we need to remove the taken piece off the board
                                #logic of calculating moves already guarantees that is there is a piece on a tile in legalmoves list, it is opponent's piece!
                                board.updateConfig(None, (piece.x, piece.y))
                            board.updateConfig(active_box, prevMove)
                            prevMove = None
                        active_box = None
                        dragging = False

                        #once player has made a legal move, we can switch turns
                        if turn == "white":
                            turn = "black"
                        else:
                            turn = "white"
                    else:
                        #if not a legal move, return piece back and don't update config
                        dragging = False
                        active_box = None
                        piece.x = prevMove[0]
                        piece.y = prevMove[1]
                else:
                    dragging = False
                    active_box = None
                    piece.x = prevMove[0]
                    piece.y = prevMove[1]
        if event.type == pygame.QUIT:
            running = False

    screen.fill((80, 115, 65))
    
    board.draw_board(screen)
    board.draw_pieces(screen)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()