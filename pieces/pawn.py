from pieces.piece import Piece
from pieces.rook import Rook
from pieces.move import Move
import copy
class Pawn(Piece):
    def __init__(self, team, type, image, row, col, killable=False):
        value = 100
        self.initialPosition = [row, col]
        super().__init__(team, type, image, value, row, col, killable)
    
    def getMoves(self, _board):
        board = _board.board
        rowI, colI = self.getPosition()
        direction = 1
        if self.team == False:
            direction = -1
        moves = []
        if board[rowI][colI] == 0:
            print("ALO")
        pieceMoved = board[rowI][colI]
        # if rowI == self.initialPosition[0] and board[rowI+direction][colI] == 0:
        if 0 <= rowI + direction <=7 and board[rowI+direction][colI] == 0:
            # move 1 square
            moves.append(Move((rowI, colI), (rowI+direction, colI), pieceMoved, 0))
            if 0 <= rowI + 2* direction <=7 and board[rowI+2*direction][colI] == 0 and self.initialPosition == [rowI, colI]:
                # move 2 squares
                moves.append(Move((rowI, colI), (rowI+2*direction, colI), pieceMoved, 0))
        
        for i in [-1, 1]:
            if (7>= colI + i >= 0 and 7>= rowI + direction >= 0) and board[rowI + direction][colI + i] != 0 and board[rowI + direction][colI + i].team != self.team:
                pieceCaptured = board[rowI + direction][colI + i]
                moves.append(Move((rowI, colI), (rowI + direction, colI + i), pieceMoved, pieceCaptured))
            # enPassant
            if (7>= colI + i >= 0 and 7>= rowI >= 0) and type(board[rowI][colI + i]) == Pawn and board[rowI][colI + i].team != self.team and board[rowI][colI + i] == _board.enPassantPiece:
                move = Move((rowI, colI), (rowI + direction, colI + i), pieceMoved, 0)
                moves.append(move)



        return moves

                
                
                

