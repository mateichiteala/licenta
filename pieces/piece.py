from abc import ABC, abstractmethod


class Piece(ABC):
    def __init__(self, team, type, image, value, row, col, killable=False):
        self.team = team  # 0 - white; 1 - black
        self.type = type  # p-pawn, N-knight, B-bishop, R-rook, Q-queen, K-king
        self.image = image
        self.value = value  # p-1, N-3, B-3, R-5, Q-9, K-INF
        self.row = row
        self.col = col

    def getPosition(self):
        return self.row, self.col

    def setPosition(self, row, col):
        self.row = row
        self.col = col

    def getImage(self):
        return self.image

    @abstractmethod
    def getMoves(self, _board):
        pass

    def __eq__(self, obj) -> bool:
        if type(obj) == type(self) and self.getPosition() == obj.getPosition():
            return True
        else:
            return False
