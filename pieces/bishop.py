from pieces.piece import Piece
from pieces.move import Move


class Bishop(Piece):
    def __init__(self, team, type, image, row, col, killable=False):
        value = 3
        super().__init__(team, type, image, value, row, col, killable)
    def getMoves(self, board):
        directions = [(1, 1), (-1, -1), (-1, 1), (1, -1)] # top-right, down-left. top-left, down-right
        moves = []
        rowI, colI = self.getPosition()
        pieceMoved = board[rowI, colI]
        for direction in directions:
            for square in range(1, 8):
                rowF = rowI + direction[0] * square
                colF = colI + direction[1] * square
                if 0 <= rowF < 8 and 0 <= colF < 8:  # inside the board 
                    pieceCaptured = board[rowF][colF]
                    if board[rowF][colF] == 0:  # empty square
                        moves.append(Move((rowI, colI), (rowF, colF), pieceMoved, pieceCaptured))
                    elif board[rowF][colF].team != self.team:  # enemy piece
                        moves.append(Move((rowI, colI), (rowF, colF), pieceMoved, pieceCaptured))
                        break
                    else: # own piece
                        break
                else: # outside the board
                    break
        return moves
