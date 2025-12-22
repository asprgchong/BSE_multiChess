from board import Board    
import pygame
import sys

WIDTH = 1500
HEIGHT = 1200

pygame.init()
screen = pygame.display.set_caption("Test Window")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
cellwidth = 120
leftPush = 40
topPush = 30

running = True
board = Board(960, 960)
board.boardSetUp()

while running:
    for event in pygame.event.get():
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 1:

        if event.type == pygame.QUIT:
            running = False

    screen.fill((80, 115, 65))
    
    board.draw_board(screen)
    board.draw_pieces(screen)
    # pygame.draw.circle(screen, (0, 150, 255), (400, 300), 50)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()