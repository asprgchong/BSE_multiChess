from board import Board 
from pieces.Rook import Rook
from pieces.Knight import Knight
from pieces.Bishop import Bishop
from pieces.Queen import Queen
from pieces.King import King
from pieces.Pawn import Pawn
import pygame
import asyncio

WIDTH = 1500
HEIGHT = 1200
pygame.init()
screen = pygame.display.set_caption("Chess Game")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

async def main():
    cellwidth = 120
    leftPush = 40
    topPush = 30
    running = True

    board = Board(960, 960)
    board.boardSetUp()

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
                        if piece.getPosition() in currPieceLegalMoves:
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
        await asyncio.sleep(0)
    pygame.quit()

asyncio.run(main())