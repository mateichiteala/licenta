
# from board import Board


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

        self.castleIndex = False # for king and rook

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
        return Move(initialPos=self.getInitialPos(), finalPos=self.getFinalPos(), pieceMoved=None, pieceCaputured=None)

    def __eq__(self, obj) -> bool:
        if self.getInitialPos() == obj.getInitialPos() and self.getFinalPos() == obj.getFinalPos()\
            and self.pieceMoved == obj.pieceMoved and self.pieceCaptured == obj.pieceCaptured:
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


def fromPNGtoMove(chessNotationMove: str, board):

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
        moves = board.getValidMoves()
        move: Move
        for move in moves:
            if move.getFinalPos() == (rowF, colF):
                initialPos = move.getInitialPos()

    if initialPos == ():
        return None
        
    return (initialPos, finalPos)


        

    