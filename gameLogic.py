from board import Board 
import queryPuzzle  
from pieces.Rook import Rook
from pieces.Knight import Knight
from pieces.Bishop import Bishop
from pieces.Queen import Queen
from pieces.King import King
from pieces.Pawn import Pawn
import pygame
import sys

WIDTH = 1500
HEIGHT = 1200

pygame.init()
screen = pygame.display.set_caption("Chess Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
cellwidth = 120
leftPush = 40
topPush = 30
notation = ['a','b','c','d','e','f','g','h']
running = True

board = Board(960, 960)
board.boardSetUp()
fen = queryPuzzle.getDaysPuzzle()

active_box = None
dragging = False
prevMove = None
currPieceLegalMoves = []
gameOver = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and not gameOver:
                ############################################################################
                ###############THIS IS FOR THE ACTIVATING PUZZLE MODE#######################
                ############################################################################
                if button.collidepoint(event.pos):
                    board.boardSetUp(FENlist=fen)
                else:
                    ############################################################################
                    ###############THIS IS FOR THE ACTUAL GAME MECHANICS########################
                    ############################################################################
                    for i, eachPiece in enumerate(board.activePieces):
                        if eachPiece.collidepoint(event.pos):
                            piece = board.pieceMapping[i][0]

                            if piece.color == board.turn:
                                active_box = i
                                currPieceLegalMoves = board.get_legal_moves_for_piece(piece)
                                print(f"Selected {piece.color} piece at {piece.getPosition()}")
                                print(f"Legal moves: {currPieceLegalMoves}")

                                if board.is_in_check(piece.color):
                                    print(f"{piece.color} king is in CHECK!")

                                prevMove = piece.getPosition()
                                dragging = True
                            else:
                                # Wrong turn: give feedback but don't select the piece,
                                # so the mouse-up handler never sees a half-set selection.
                                print(f"It's {board.turn}'s turn!")
                                active_box = None
                            break
                    ############################################################################
                    ###############THIS IS FOR THE ACTUAL GAME MECHANICS########################
                    ############################################################################
                            
        if event.type == pygame.MOUSEMOTION:
            ############################################################################
            ###############THIS IS FOR THE ACTUAL GAME MECHANICS########################
            ############################################################################
            if active_box is not None and dragging and not gameOver:
                piece = board.pieceMapping[active_box][0]
                piece.x = (event.pos[0] - leftPush) // cellwidth
                piece.y = (event.pos[1] - topPush) // cellwidth
            ############################################################################
            ###############THIS IS FOR THE ACTUAL GAME MECHANICS########################
            ############################################################################
                
        if event.type == pygame.MOUSEBUTTONUP:
            ############################################################################
            ###############THIS IS FOR THE ACTUAL GAME MECHANICS########################
            ############################################################################
            if event.button == 1 and active_box is not None and not gameOver:
                piece = board.pieceMapping[active_box][0]
                if piece.color == board.turn:
                    ############################################################################
                    ###############THIS IS FOR THE ACTUAL PUZZLE SIM############################
                    ############################################################################
                    if board.puzzleSolution != [] and (piece.x, piece.y) == board.puzzleSolution[0]["pos"]:
                        # print(board.puzzleSolution)
                        checkProps = board.puzzleSolution[0]
                        if (checkProps["piece"] == "R" and isinstance(piece,Rook)) or (checkProps["piece"] == "N" and isinstance(piece, Knight)) or (checkProps['piece'] == "P" and isinstance(piece, Pawn)) or (checkProps['piece'] == "Q" and isinstance(piece, Queen) or (checkProps["piece"] == "B" and isinstance(piece, Bishop)) or (checkProps['piece'] == "K" and isinstance(piece, King))):
                            if piece.color == board.puzzleStart:
                                if checkProps["capture"]:
                                    oppPiece = board.config[piece.y][piece.x].getCurrentOccupyingPiece()
                                    board.updateConfig(board.pieceMapping.index((oppPiece, 1)), (piece.x, piece.y), True)
                                board.updateConfig(active_box, prevMove)
                                if checkProps['mate']:
                                    winner = "black" if board.turn == "black" else "white"
                                    board.turn = "black" if board.turn == "white" else "black"
                                    print(f"Checkmate! {winner} wins!")
                                    gameOver = True
                                board.puzzleSolution.pop(0)
                        prevMove = None
                        active_box = None
                        dragging = False
                        currPieceLegalMoves = []

                        # Simulate next move
                        if board.puzzleSolution != []:
                            newProps = board.puzzleSolution[0]
                            print(newProps)
                            target = newProps['pos']
                            # Find the moving piece FIRST (before removing any captured
                            # piece), so that pawn captures still register as legal moves.
                            x, y = None, None
                            piece = None
                            if newProps['row'] is not None:
                                # disambiguator is a file letter -> fixes the column (x)
                                x = notation.index(newProps['row'])
                                for yindex, rowlist in enumerate(board.config):
                                    p = rowlist[x].getCurrentOccupyingPiece()
                                    if (newProps["piece"] == "R" and isinstance(p,Rook)) or (newProps["piece"] == "N" and isinstance(p, Knight)) or (newProps['piece'] == "P" and isinstance(p, Pawn)) or (newProps['piece'] == "Q" and isinstance(p, Queen) or (newProps["piece"] == "B" and isinstance(p, Bishop)) or (newProps['piece'] == "K" and isinstance(p, King))):
                                        if target in p.get_legal_moves(board):
                                            y = yindex
                                            piece = p
                                            break
                            elif newProps['col'] is not None:
                                # disambiguator is a rank number -> fixes the row (y)
                                y = 7 - (newProps['col'] - 1)
                                for xindex, tile in enumerate(board.config[y]):
                                    p = tile.getCurrentOccupyingPiece()
                                    if (newProps["piece"] == "R" and isinstance(p,Rook)) or (newProps["piece"] == "N" and isinstance(p, Knight)) or (newProps['piece'] == "P" and isinstance(p, Pawn)) or (newProps['piece'] == "Q" and isinstance(p, Queen) or (newProps["piece"] == "B" and isinstance(p, Bishop)) or (newProps['piece'] == "K" and isinstance(p, King))):
                                        if target in p.get_legal_moves(board):
                                            x = xindex
                                            piece = p
                                            break
                            else:
                                for rindex, row in enumerate(board.config):
                                    for cindex, col in enumerate(row):
                                        p = col.getCurrentOccupyingPiece()
                                        if (newProps["piece"] == "R" and isinstance(p,Rook)) or (newProps["piece"] == "N" and isinstance(p, Knight)) or (newProps['piece'] == "P" and isinstance(p, Pawn)) or (newProps['piece'] == "Q" and isinstance(p, Queen) or (newProps["piece"] == "B" and isinstance(p, Bishop)) or (newProps['piece'] == "K" and isinstance(p, King))):
                                            if target in p.get_legal_moves(board):
                                                x = cindex
                                                y = rindex
                                                piece = p
                                                break
                                    if piece is not None:
                                        break

                            # Now that the mover is known, remove the captured piece (if any).
                            #Completes user move.
                            if newProps['capture']:
                                captured = board.config[target[1]][target[0]].getCurrentOccupyingPiece()
                                pieceToCapture = board.pieceMapping.index((captured, 1))
                                board.updateConfig(pieceToCapture, target, True)

                            pygame.time.delay(1000)
                            # simulate puzzle response
                            piece.x = target[0]
                            piece.y = target[1]
                            index = board.pieceMapping.index((piece,1))
                            board.updateConfig(index, (x, y))
                            board.puzzleSolution.pop(0)
                    ############################################################################
                    ###############THIS IS FOR THE ACTUAL PUZZLE SIM############################
                    ############################################################################
                    elif piece.getPosition() in currPieceLegalMoves and board.puzzleSolution == []:
                        if prevMove is not None and (piece.x != prevMove[0] or piece.y != prevMove[1]):
                            oppPiece = board.config[piece.y][piece.x].getCurrentOccupyingPiece()
                            if oppPiece is not None and oppPiece.color != piece.color:
                                board.updateConfig(board.pieceMapping.index((oppPiece, 1)), (piece.x, piece.y), True)
                            elif oppPiece is None and isinstance(piece,Pawn):
                                if piece.color == "white":
                                    if board.config[piece.y + 1][piece.x].getCurrentOccupyingPiece() in board.blackenpassants:
                                        board.updateConfig(board.pieceMapping.index((board.config[piece.y+1][piece.x].getCurrentOccupyingPiece(),1)), (piece.x, piece.y+1), True)
                                else:
                                    if board.config[piece.y - 1][piece.x].getCurrentOccupyingPiece() in board.whiteenpassants:
                                        board.updateConfig(board.pieceMapping.index((board.config[piece.y-1][piece.x].getCurrentOccupyingPiece(),1)), (piece.x, piece.y-1), True)
                            board.updateConfig(active_box, prevMove)

                            # Switch turns!!
                            board.turn = "black" if board.turn == "white" else "white"
                            
                            # Checking for checkmate/stalemate
                            result = board.checkmate("white" if board.turn == "black" else "black")
                            if result == "stalemate":
                                print("Stalemate!")
                                gameOver = True
                            elif result == "checkmate":
                                winner = "white" if board.turn == "black" else "black"
                                print(f"Checkmate! {winner} wins!")
                                gameOver = True
                            elif board.is_in_check(board.turn):
                                print(f"{board.turn} is in CHECK!")
                            
                            print(f"Turn: {board.turn}")
                        
                        prevMove = None
                        active_box = None
                        dragging = False
                        currPieceLegalMoves = []
                    else:
                        if board.puzzleSolution != []:
                            print("Not the puzzle solution! Try again.")
                        else:
                            print("Invalid move!")
                        if prevMove is not None:
                            piece.x = prevMove[0]
                            piece.y = prevMove[1]
                        prevMove = None
                        active_box = None
                        dragging = False
                        currPieceLegalMoves = []
            ############################################################################
            ###############THIS IS FOR THE ACTUAL GAME MECHANICS########################
            ############################################################################

        if event.type == pygame.QUIT:
            running = False

    ############################################################################
    ###################SETTING UP THE UI FOR THE GAME###########################
    ############################################################################
    screen.fill((80, 115, 65))
    # Button for puzzle set up
    button = pygame.draw.rect(screen, pygame.Color(0, 0, 0,1), (960 + (leftPush * 1.5), topPush, cellwidth * 3.8, cellwidth * 0.75))  
    font = pygame.font.Font(None, 40)
    text = font.render("Play Today Chess.com Puzzle", False, (255, 255, 255))
    screen.blit(text, ((960 + (leftPush * 2) + 20), (topPush + 20)))

    # Translucent black panel directly below the puzzle button.
    # Drawn on its own SRCALPHA surface so the alpha channel is respected.
    panel_x = 960 + (leftPush*1.5)
    panel_y = topPush + (cellwidth * 0.75) + 10   # just under the button
    panel_width = cellwidth * 3.8                    # same width as the button
    panel_height = cellwidth * 8
    panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    panel.fill((0, 0, 0, 150))   # RGBA — last value is alpha (0=clear, 255=solid)
    screen.blit(panel, (panel_x, panel_y))

    board.draw_board(screen)
    board.draw_pieces(screen)
    board.displayCapturedPieces(screen)
    # Make the button to indicate that we want to set up the puzzle on the board

    if gameOver:
        # Display game over message
        font = pygame.font.Font(None, 72)
        if board.checkmate("white" if board.turn == "black" else "black") == "checkmate":
            winner = "White" if board.turn == "black" else "Black"
            result_text = f"Checkmate! {winner} Wins!"
        else:
            result_text = "Stalemate!"
        text = font.render(result_text, True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
        
        # Draw background for text
        bg_rect = text_rect.inflate(20, 20)
        pygame.draw.rect(screen, (255, 255, 255), bg_rect)
        pygame.draw.rect(screen, (0, 0, 0), bg_rect, 3)
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
sys.exit()