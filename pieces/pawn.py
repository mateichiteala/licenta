from pieces.piece import Piece
from pieces.move import Move


class Pawn(Piece):
    def __init__(self, team, row, col, initilialPosSet=True):
        value = 100
        type = 'p'
        if initilialPosSet == True:
            self.initialPosition = [row, col]
        else:
            self.initialPosition = [-1, -1]

        super().__init__(team, type, value, row, col)


    def getMoves(self, _board):
        board = _board.board
        rowI, colI = self.getPosition()
        direction = -1
        if self.team == False:
            direction = 1
        moves = []
        pieceMoved = board[rowI][colI]
        if 0 <= rowI + direction <= 7 and board[rowI+direction][colI] == 0:
            # move 1 square
            moves.append(
                Move((rowI, colI), (rowI+direction, colI), pieceMoved, 0))
            if 0 <= rowI + 2 * direction <= 7 and board[rowI+2*direction][colI] == 0 \
                    and self.initialPosition == [rowI, colI]:
                # move 2 squares
                moves.append(
                    Move((rowI, colI), (rowI+2*direction, colI), pieceMoved, 0))

        for i in [-1, 1]:
            # capture
            if (7 >= colI + i >= 0 and 7 >= rowI + direction >= 0) and board[rowI + direction][colI + i] != 0 \
                    and board[rowI + direction][colI + i].team != self.team:
                pieceCaptured = board[rowI + direction][colI + i]
                moves.append(Move((rowI, colI), (rowI + direction,
                             colI + i), pieceMoved, pieceCaptured))

            # enPassant
            if (7 >= colI + i >= 0 and 7 >= rowI >= 0) and type(board[rowI][colI + i]) == Pawn \
                    and board[rowI][colI + i].team != self.team and board[rowI][colI + i] == _board.enPassantPiece:
                pieceCaptured = board[rowI][colI + i]
                move = Move((rowI, colI), (rowI + direction,
                            colI + i), pieceMoved, pieceCaptured)
                moves.append(move)
        return moves
