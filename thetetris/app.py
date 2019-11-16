import pygame
import time
import thetetris.constants as constants
import thetetris.grid as grid
import thetetris.pieces as pieces
import thetetris.window as window


def run():
    # initialization
    win = window.createWindow(constants.width, constants.height)
    run = True
    g = grid.Grid()

    # pieces
    curPiece = pieces.getPiece()
    nextPiece = pieces.getPiece()

    # drawings

    clock = pygame.time.Clock()

    startTime = time.time()
    while run:
        clock.tick(100)
        if time.time() - startTime >= 1:
            curPiece.y += 1
            startTime = time.time()
        g.updateGrid(curPiece)
        window.updateWindow(win, g)
        for event in pygame.event.get():
            pressedKey = None
            if event.type == pygame.KEYDOWN:
                pressedKey = event.key
            curPiece.transform(pressedKey)
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

    print("Bye")
