from pieces.bishop import Bishop
from pieces.piece import Piece
from pieces.bishop import Bishop
from pieces.rook import Rook

class Queen(Piece):
    def __init__(self, team, type, image, row, col, killable=False):
        value = 9
        super().__init__(team, type, image, value, row, col, killable)
    def getMoves(self, board):
        # rook + bishop
        rowI, colI = self.getPosition()
        return Bishop(self.team, 'B', 0, rowI, colI, False).getMoves(board) + Rook(self.team, 'R', 0, rowI, colI, False).getMoves(board)