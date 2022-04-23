from pieces.piece import Piece
from pieces.move import Move

class King(Piece):
    def __init__(self, team, type, image, row, col, killable=False):
        value = -1
        super().__init__(team, type, image, value, row, col, killable)
    def getMoves(self, _board):
        board = _board.board
        directions = [(1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
        moves = []
        rowI, colI = self.getPosition()
        pieceMoved = board[rowI][colI]
        for direction in directions:
            rowF = rowI + direction[0]
            colF = colI + direction[1]
            if 0 <= rowF < 8 and 0 <= colF < 8 and (board[rowF][colF] == 0 or board[rowF][colF].team != self.team):
                pieceCaptured = board[rowF][colF]
                moves.append(Move((rowI, colI), (rowF, colF), pieceMoved, pieceCaptured))
        return moves