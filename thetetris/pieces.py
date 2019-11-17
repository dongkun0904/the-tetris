import pygame
import random
import thetetris.constants as constants


class Piece:
    def __init__(self, x, y, piece, rotation):
        self.x = x
        self.y = y
        self.type = piece
        self.variations = len(constants.pieces[piece])
        self.piece = constants.pieces[piece]
        self.color = constants.pieceColors[piece]
        self.rotation = rotation

        # calculate the width and height of the piece
        self.calculateSize()

    def tick(self, placedBlocks):
        placed = False
        self.y += 1
        if self._checkCollision(placedBlocks):
            self.y -= 1
            placed = True

        return placed

    """
    Validation function for transformations
    It handles the case where the piece goes out of the grid.
    It returns true if there is a conflict between the current piece
    and the existing placed blocks
    """

    def _checkCollision(self, placedBlocks):
        # ensure the width and height are correct
        self.calculateSize()

        if self.x < -self.leftStart:
            self.x = -self.leftStart

        if self.x > constants.columns - self.width - self.leftStart:
            self.x = constants.columns - self.width - self.leftStart

        print("({}, {})".format(self.x, self.y))

        if self.y > constants.rows - self.height - self.topStart:
            return True

        p = self.piece[self.rotation]

        for i in range(len(p)):
            for j in range(len(p[i])):
                if p[i][j] == '0' and (j + self.x, i + self.y) in placedBlocks:
                    return True

        return False

    def calculateSize(self):
        # calculate the width and height of the piece
        minX = 4
        maxX = 0
        height = 0
        minY = 0
        for row in self.piece[self.rotation]:
            if row != '.....':
                minX = min(minX, row.find('0'))
                maxX = max(maxX, row.rfind('0'))
                height += 1
        for row in self.piece[self.rotation]:
            if row != '.....':
                break
            minY += 1
        self.width = maxX - minX + 1
        self.height = height
        self.leftStart = minX
        self.topStart = minY

    """
    transform returns true if the piece is placed
    """

    def transform(self, pressedKey, placedBlocks):
        placed = False
        if pressedKey == pygame.K_LEFT:
            self.x -= 1

            # if there was a block already
            if self._checkCollision(placedBlocks):
                self.x += 1

        elif pressedKey == pygame.K_RIGHT:
            self.x += 1

            # if there was a block already
            if self._checkCollision(placedBlocks):
                self.x -= 1

        elif pressedKey == pygame.K_DOWN:
            self.y += 1

            # if there was a block already
            if self._checkCollision(placedBlocks):
                self.y -= 1
                placed = True

        elif pressedKey == pygame.K_z:
            self.rotation -= 1
            self.rotation = self.rotation % self.variations

            # if there was a block already
            if self._checkCollision(placedBlocks):
                self.rotation += 1
                self.rotation = self.rotation % self.variations

        elif pressedKey == pygame.K_x:
            self.rotation += 1
            self.rotation = self.rotation % self.variations
            if self._checkCollision(placedBlocks):
                self.rotation -= 1
                self.rotation = self.rotation % self.variations

        elif pressedKey == pygame.K_SPACE:
            placed = True
            mock = self.getLandingPlace(placedBlocks)
            self.y = mock.y
        self.calculateSize()

        return placed

    # TODO: need to catch the case where we can put the piece under the existing ones
    def getLandingPlace(self, placedBlocks):
        mock = Piece(self.x, self.y, self.type, self.rotation)
        while not mock._checkCollision(placedBlocks):
            mock.y += 1
        mock.y -= 1
        return mock

    def registerPiece(self, placedBlocks):
        p = self.piece[self.rotation]

        for i in range(len(p)):
            for j in range(len(p[i])):
                if p[i][j] == '0':
                    placedBlocks[(j + self.x, i + self.y)] = self.color


def getPiece():
    return Piece(3, -1, random.randint(0, 6), 0)
