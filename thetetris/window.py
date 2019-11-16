import pygame
import thetetris.constants as constants


def createWindow(width, height):
    # icon = pygame.image.load("")
    # pygame.display.set_icon(icon)
    pygame.display.set_caption("The Tetris")

    window = pygame.display.set_mode((width, height))
    window.fill((255, 255, 255))

    return window


def updateWindow(window, grid):
    window.fill((255, 255, 255))
    for i in range(len(grid.cells)):
        for j in range(len(grid.cells[i])):
            pygame.draw.rect(window, grid.cells[i][j], (constants.topLeftX + (
                j * constants.unit), constants.topLeftY + (i * constants.unit), constants.unit, constants.unit))
    pygame.display.update()
