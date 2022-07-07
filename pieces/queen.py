from pieces.bishop import Bishop
from pieces.piece import Piece
from pieces.bishop import Bishop
from pieces.rook import Rook

class Queen(Piece):
    def __init__(self, team, row, col):
        value = 900
        type = 'Q'
        super().__init__(team, type, value, row, col)

    def getMoves(self, _board):
        # rook + bishop
        rowI, colI = self.getPosition()
        return Bishop(self.team, rowI, colI).getMoves(_board) + Rook(self.team, rowI, colI).getMoves(_board)