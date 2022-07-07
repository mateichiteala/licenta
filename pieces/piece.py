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
