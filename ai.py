from abc import ABC, abstractmethod

class AI(ABC):
    @abstractmethod
    def getBestMoveAI(self):
        pass
    @abstractmethod
    def updateDatabase(self):
        pass
