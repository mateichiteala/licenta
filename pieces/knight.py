import imp
from pieces.piece import Piece
from pieces.move import Move


class Knight(Piece):
    def __init__(self, team, type, image, row, col, killable=False):
        value = 3
        super().__init__(team, type, image, value, row, col, killable)
    def getMoves(self, board):
        directions = [(1, -2), (1, 2), (-1, -2), (-1, 2), (2, -1), (2, 1), (-2, -1), (-2, 1)]
        moves = []
        rowI, colI = self.getPosition()
        pieceMoved = board[rowI, colI]
        for direction in directions:
            rowF = rowI + direction[0]
            colF = colI + direction[1]
            if (0 <= rowF < 8 and 0 <= colF < 8) and (board[rowF][colF] == 0 or board[rowF][colF].team != self.team):  # inside the board, empty square or enemy piece 
                pieceCaptured = board[rowF][colF]
                moves.append(Move((rowI, colI), (rowF, colF), pieceMoved, pieceCaptured))
        return moves