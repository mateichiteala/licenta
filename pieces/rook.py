from pieces.piece import Piece
from pieces.move import Move

class Rook(Piece):
    def __init__(self, team, row, col):
        value = 500
        type = 'R'
        self.castle = True
        self.firstMoveIndex = None
        super().__init__(team, type, value, row, col)

    def setCastle(self, castle: True):
        self.castle = castle
        
    def getMoves(self, _board):
        board = _board.board
        moves = []
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)] #  up, down, left, right
        rowI, colI = self.getPosition()
        pieceMoved = board[rowI, colI]

        for direction in directions:
            for square in range(1, 8):
                rowF = rowI + direction[0] * square
                colF = colI + direction[1] * square
                if 0 <= rowF < 8 and 0 <= colF < 8:  # inside the board 
                    pieceCaptured = board[rowF][colF]
                    if board[rowF][colF] == 0:  # empty square
                        moves.append(
                            Move((rowI, colI), (rowF, colF),pieceMoved, pieceCaptured))
                        # enemy piece and stop searching on that row, col
                    elif board[rowF][colF].team != self.team: 
                        moves.append(
                            Move((rowI, colI), (rowF, colF), pieceMoved, pieceCaptured))
                        break 
                    else: # my own piece and stop searching on that row, col
                        break
                else: #  outside the board stop searching on that row, col
                    break
        return moves

