from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, team, type, value, row, col):
        self.team: bool = team  # True - white; False - black
        self.type: str = type  # p-pawn, N-knight, B-bishop, R-rook, Q-queen, K-king
        self.value: float = value  # p-100, N-300, B-330, R-500, Q-900, K-INF
        self.row: int = row
        self.col: int = col

    def getPosition(self):
        return self.row, self.col

    def setPosition(self, row, col):
        self.row = row
        self.col = col

    @abstractmethod
    def getMoves(self, _board):
        pass

    def __eq__(self, obj) -> bool:
        if type(obj) == type(self) and self.getPosition() == obj.getPosition():
            return True
        else:
            return False
class Pawn(Piece):
    def __init__(self, team, type, row, col):
        value = 100
        self.initialPosition = [row, col]
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
class Bishop(Piece):
    def __init__(self, team, type, row, col):
        value = 330
        super().__init__(team, type, value, row, col)

    def getMoves(self, _board):
        board = _board.board
        directions = [(1, 1), (-1, -1), (-1, 1), (1, -1)]  # top-right, down-left. top-left, down-right
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
                    else:  # own piece
                        break
                else:  # outside the board
                    break
        return moves
class King(Piece):
    def __init__(self, team, type, row, col):
        value = 20000
        self.castle = True  # on false if king moved
        self.inCastle = False
        self.firstMoveIndex = None
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
                        inc = 1 if i == 3 else -1
                        moves_castle = []

                        for j in range(inc, i, inc):
                            if board[rowI][colI + j] != 0:
                                empty = False
                                break
                            if i == -4:
                                moves_castle.append(Move((rowI, colI + j + 1), (rowI, colI + j), pieceMoved, 0))
                            else:
                                moves_castle.append(Move((rowI, colI + j - 1), (rowI, colI + j), pieceMoved, 0))

                        # check if the empty squares are attacked
                        check = False
                        if empty:
                            self.inCastle = True
                            move: Move
                            for index, move in enumerate(moves_castle):
                                _board.move(move)
                                checks, pins, attackPins = _board.getChecksAndPins(self.team)
                                if len(checks) > 0:
                                    _index = index
                                    while _index >= 0:
                                        _board.undoMove()
                                        _index -= 1
                                    self.inCastle = False
                                    check = True
                                    break

                            # the empty squares are not attacked
                            # undo moves
                            if check == False:
                                for _ in moves_castle:
                                    _board.undoMove()
                                moves.append(Move((rowI, colI), (rowI, colI + i), pieceMoved, rook))
                                self.inCastle = False

        return moves

class Move():
    def __init__(self, initialPos, finalPos, pieceMoved=0, pieceCaputured=0):
        self.rowI = initialPos[0]
        self.colI = initialPos[1]
        self.rowF = finalPos[0]
        self.colF = finalPos[1]

        self.pieceMoved = pieceMoved
        self.pieceCaptured = pieceCaputured

        self.enPassantPiece = 0
        self.enPassantActive = 0

        self.castleIndex = False  # for king and rook

    def get(self):
        return (self.rowI, self.colI), (self.rowF, self.colF)

    def getInitialPos(self):
        return (self.rowI, self.colI)

    def getFinalPos(self):
        return (self.rowF, self.colF)

    def getPieceMoved(self):
        return self.pieceMoved

    def getPieceCaptured(self):
        return self.pieceCaptured

    def setPieceMoved(self, pieceMoved):
        self.pieceMoved = pieceMoved

    def setPieceCaptured(self, pieceCaptured):
        self.pieceCaptured = pieceCaptured

    def copy(self):
        return Move(initialPos=self.getInitialPos(), finalPos=self.getFinalPos(), pieceMoved=None,
                    pieceCaputured=None)

    def __eq__(self, obj) -> bool:
        if self.getInitialPos() == obj.getInitialPos() and self.getFinalPos() == obj.getFinalPos():
            return True
        else:
            return False

    def getChessNotationMove(self):
        row, col = self.getInitialPos()
        col = chr(col + 97)
        row += 1
        initial = f"{col}{row}"

        row, col = self.getFinalPos()
        col = chr(col + 97)
        row += 1
        final = f"{col}{row}"

        return initial, final

    def fromMoveToPNG(self):
        _, finalPos = self.getChessNotationMove()
        result = ""

        if self.pieceMoved.type == "K" and self.pieceCaptured != 0 and self.pieceCaptured.type == "R" and self.pieceCaptured.team == self.pieceCaptured.team:
            if self.pieceCaptured.col == 0:
                return "O-O-O"
            else:
                return "O-O"

        if self.pieceMoved.type != "p":
            result += self.pieceMoved.type

        if self.pieceCaptured != 0:
            # print(self.pieceCaptured)
            result += "x"

        result += finalPos

        return result
def fromPNGtoMove(chessNotationMove: str, board, pins):

    if "O-O" == chessNotationMove:
        initialPos = (0, 4)
        if board.playerTurn:
            finalPos = (0, 7)
        else:
            finalPos = (7, 7)
        return (initialPos, finalPos)

    if "O-O-O" == chessNotationMove:
        initialPos = (0, 4)
        if board.playerTurn:
            finalPos = (0, 0)
        else:
            finalPos = (7, 0)
        return (initialPos, finalPos)

    pieceType = chessNotationMove[0]
    finalPosChessNotation = chessNotationMove[-2:]
    # print(finalPosChessNotation)
    rowF = 8 - int(finalPosChessNotation[1])
    colF = ord(finalPosChessNotation[0]) - 97
    initialPos = ()
    finalPos = (rowF, colF)

    if chessNotationMove[0] not in ["N", "B", "R", "Q", "K"]:
        # mutam pionul
        pieceType = "p"

    # toate piesele cu tipul necesar + echipa
    pieces = board.getAllPiecesByTypeAndTurn(pieceType, board.playerTurn)

    for piece in pieces:
        moves = board.allValidMoves(board.playerTurn, pins)
        move: Move
        for move in moves:
            if move.getFinalPos() == (rowF, colF):
                initialPos = move.getInitialPos()

    if initialPos == ():
        return None

    return (initialPos, finalPos)
class Queen(Piece):
    def __init__(self, team, type, row, col):
        value = 900
        super().__init__(team, type, value, row, col)

    def getMoves(self, _board):
        # rook + bishop
        rowI, colI = self.getPosition()
        return Bishop(self.team, 'B', rowI, colI).getMoves(_board) + Rook(self.team, 'R', rowI, colI).getMoves(_board)


class Rook(Piece):
    def __init__(self, team, type, row, col):
        value = 500
        self.castle = True
        self.firstMoveIndex = None
        super().__init__(team, type, value, row, col)

    def setCastle(self, castle: True):
        self.castle = castle

    def getMoves(self, _board):
        board = _board.board
        moves = []
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # up, down, left, right
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
                            Move((rowI, colI), (rowF, colF), pieceMoved, pieceCaptured))
                        # enemy piece and stop searching on that row, col
                    elif board[rowF][colF].team != self.team:
                        moves.append(
                            Move((rowI, colI), (rowF, colF), pieceMoved, pieceCaptured))
                        break
                    else:  # my own piece and stop searching on that row, col
                        break
                else:  # outside the board stop searching on that row, col
                    break
        return moves



