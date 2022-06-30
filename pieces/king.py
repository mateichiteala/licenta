from pieces.piece import Piece
from pieces.move import Move
from pieces.rook import Rook

class King(Piece):
    def __init__(self, team, type, row, col):
        value = 20000
        self.castle = True  # on false if king moved
        self.inCastle = False
        super().__init__(team, type, value, row, col)
    

    def setCastle(self, castle: True):
        self.castle = castle
        
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
        
        # check castle
        if self.castle and (self.inCastle is False):
            for i in [-4, 3]:
                # print(rowI, colI)
                if 0 <= rowI < 8 and 0 <= colI + i < 8:
                    rook: Rook = board[rowI][colI + i] 
                    if type(rook) == Rook and rook.castle:
                        # check if are empty squares between king and rook
                        empty = True
                        inc = 1 if i==3 else -1
                        moves_castle = []
                        
                        for j in range(inc, i, inc):
                            if board[rowI][colI+j] != 0:
                                empty = False
                                break
                            if i == -4:
                                moves_castle.append(Move((rowI, colI + j + 1), (rowI, colI + j), pieceMoved, 0))
                            else:
                                moves_castle.append(Move((rowI, colI + j - 1), (rowI, colI + j), pieceMoved, 0))
                                
                        # check if the empty squares are attacked
                        check = True
                        if empty:
                            self.inCastle = True
                            move: Move
                            for index, move in enumerate(moves_castle):
                                _board.move(move)
                                # _board.printBoard()
                                _, check, _= _board.isCheck(self.team)
                                if check:
                                    _index = index
                                    while _index >= 0:
                                        _board.undoMove()
                                        _index -= 1
                                    self.inCastle = False
                                    break
                            # the empty squares are not attacked
                            # undo moves
                            if check == False:
                                for _ in moves_castle:
                                    _board.undoMove()
                                moves.append(Move((rowI, colI), (rowI, colI + i), pieceMoved, rook))
                                self.inCastle = False


                            
        return moves