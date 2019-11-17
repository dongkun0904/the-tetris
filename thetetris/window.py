import pygame
import thetetris.constants as constants


def createWindow(width, height):
    # icon = pygame.image.load('')
    # pygame.display.set_icon(icon)
    pygame.display.set_caption(constants.TITLE)

    window = pygame.display.set_mode((width, height))
    window.fill((255, 255, 255))

    return window


def updateWindow(window, grid, nextPiece, savedPiece, text):
    window.fill((255, 255, 255))
    # updating main grid
    for i in range(len(grid.cells)):
        for j in range(len(grid.cells[i])):
            s = pygame.Surface((constants.unit, constants.unit))
            # check if the block needs alpha value
            if len(grid.cells[i][j]) > 3:
                s.set_alpha(grid.cells[i][j][3])

            s.fill(grid.cells[i][j])
            window.blit(s, (constants.topLeftX + (j * constants.unit),
                            constants.topLeftY + (i * constants.unit)))

    # updating next piece
    for i in range(len(nextPiece.piece[0])):
        for j in range(len(nextPiece.piece[0][i])):
            if nextPiece.piece[0][i][j] == '.':
                pygame.draw.rect(window, (0, 0, 0), (constants.nextPieceX + (j * constants.unit),
                                                     constants.nextPieceY + (i * constants.unit), constants.unit, constants.unit))
            else:
                pygame.draw.rect(window, nextPiece.color, (constants.nextPieceX + (j * constants.unit),
                                                           constants.nextPieceY + (i * constants.unit), constants.unit, constants.unit))

    # updating saved piece
    if savedPiece:
        for i in range(len(savedPiece.piece[0])):
            for j in range(len(savedPiece.piece[0][i])):
                if savedPiece.piece[0][i][j] == '.':
                    pygame.draw.rect(window, (0, 0, 0), (constants.savedPieceX + (j * constants.unit),
                                                         constants.savedPieceY + (i * constants.unit), constants.unit, constants.unit))
                else:
                    pygame.draw.rect(window, savedPiece.color, (constants.savedPieceX + (j * constants.unit),
                                                                constants.savedPieceY + (i * constants.unit), constants.unit, constants.unit))
    else:
        for i in range(5):
            for j in range(5):
                pygame.draw.rect(window, (0, 0, 0), (constants.savedPieceX + (j * constants.unit),
                                                     constants.savedPieceY + (i * constants.unit), constants.unit, constants.unit))

    # draw grid lines
    for i in range(1, constants.columns):
        start = (i * constants.unit + constants.topLeftX, constants.topLeftY)
        end = (i * constants.unit + constants.topLeftX,
               constants.topLeftY + constants.playHeight)
        pygame.draw.line(window, constants.unbreakableColor, start, end)

    # draw grid lines
    for i in range(1, constants.rows):
        start = (constants.topLeftX, i * constants.unit + constants.topLeftY)
        end = (constants.topLeftX + constants.playWidth,
               i * constants.unit + constants.topLeftY)
        pygame.draw.line(window, constants.unbreakableColor, start, end)

    # updating text
    window.blit(text, (constants.width // 2 - text.get_width() //
                       2, 50 - text.get_height() // 2))
    pygame.display.update()
