import thetetris.constants as constants
import thetetris.pieces as pieces


class Grid:

    def __init__(self):
        self.cells = [[(0, 0, 0) for row in range(constants.columns)]
                      for col in range(constants.rows)]

    def updateGrid(self, placed, piece):
        # reset the grid
        self.cells = [[(0, 0, 0) for row in range(constants.columns)]
                      for col in range(constants.rows)]

        # placed pieces
        for cell in placed:
            self.cells[cell[1]][cell[0]] = placed[cell]

        # floating piece
        p = piece.piece[piece.rotation]
        for i in range(len(p)):
            for j in range(len(p[i])):
                if p[i][j] == '0' and i + piece.y >= 0:
                    self.cells[i + piece.y][j + piece.x] = piece.color

        # draw the mock piece
        mock = piece.getLandingPlace(placed)
        mock.color = constants.mockColors[mock.type]
        m = mock.piece[mock.rotation]
        for i in range(len(m)):
            for j in range(len(m[i])):
                if m[i][j] == '0':
                    self.cells[i + mock.y][j + mock.x] = mock.color

    def _checkEmptyRow(self, i):
        for cell in self.cells[i]:
            if cell != (0, 0, 0):
                return False
        return True

    def _addRow(self, i):
        for x in range(len(self.cells[i])):
            self.cells[i][x] = constants.unbreakableColor

    def addExtraRow(self, n):
        # check if adding n rows to the grid is ok
        for i in range(n):
            if not self._checkEmptyRow(i):
                return True  # Game over

        # shift the blocks n times up
        for i in range(len(self.cells) - n):
            self.cells[i] = self.cells[i + n]

        # add unbreakable blocks at the end
        for i in range(n):
            self._addRow(constants.rows - i - 1)


def lost(placedBlocks):
    for block in placedBlocks:
        if block[0] >= constants.rows:
            return True

    return False
