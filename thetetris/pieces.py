import pygame
import random
import thetetris.constants as constants


class Piece:
    def __init__(self, x, y, piece):
        self.x = x
        self.y = y
        self.variations = len(constants.pieces[piece])
        self.piece = constants.pieces[piece]
        self.color = constants.pieceColors[piece]
        self.rotation = 0

    def transform(self, pressedKey):
        if pressedKey == pygame.K_LEFT:
            self.x -= 1

        if pressedKey == pygame.K_RIGHT:
            self.x += 1

        if pressedKey == pygame.K_DOWN:
            self.y += 1

        if pressedKey == pygame.K_z:
            self.rotation -= 1
            self.rotation = self.rotation % self.variations

        if pressedKey == pygame.K_x:
            self.rotation += 1
            self.rotation = self.rotation % self.variations


def getPiece():
    return Piece(3, 0, random.randint(0, 6))
