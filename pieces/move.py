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
        if self.getInitialPos() == obj.getInitialPos() and self.getFinalPos() == obj.getFinalPos():
            return True
        else:
            return False
    