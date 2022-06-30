from pieces.bishop import Bishop
from pieces.piece import Piece
from pieces.bishop import Bishop
from pieces.rook import Rook

class Queen(Piece):
    def __init__(self, team, type, row, col):
        value = 900
        super().__init__(team, type, value, row, col)

    def getMoves(self, _board):
        # rook + bishop
        rowI, colI = self.getPosition()
        return Bishop(self.team, 'B', rowI, colI).getMoves(_board) + Rook(self.team, 'R', rowI, colI).getMoves(_board)