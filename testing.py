from ai import bestMoveMinMax
from board import Board, CODE_CHECK, CODE_CHECKMATE, CODE_STALEMATE
from monteCarlo import MonteCarloTreeSearchNode

import matplotlib.pyplot as plt

class Testing():
    def __init__(self) -> None:
        self.board: Board = Board()
        self.blackWins = 0
        self.whiteWins = 0
        self.draws = 0
        self.movesPerGame = []
    def printStatistics(self):
        print(self.whiteWins, self.blackWins, self.draws)
        print(self.movesPerGame)

    def printStatus(self):
        resp = self.board.status
        if resp == CODE_CHECK:
            print("CHECK")
        if resp == CODE_CHECKMATE:
            print("CHECKMATE")
        if resp == CODE_STALEMATE:
            print("STALEMATE")
    def testing(self, samples: int, depth: int, simulations: int, time: int):
        for i in range(samples):
            movesGame = 0
            # simulations += 500
            # depth += 1
            time += 60
            while self.board.status not in [CODE_CHECKMATE, CODE_STALEMATE]: 
                self.board.printBoard()
                # aiMove = bestMoveMinMax(self.board, self.board.getValidMoves(), depth, _time=0)
                aiMove = MonteCarloTreeSearchNode(board=self.board, _depth_rollout=depth, _time=time, _sim=simulations).best_move()

                self.board.aiToBoard(aiMove)
                movesGame += 1
                self.board.printBoard()
                self.printStatus()
                print(movesGame)
                if self.board.status == CODE_CHECKMATE:
                    self.whiteWins += 1
                    self.movesPerGame.append(movesGame)

                    self.board = Board()
                    break
                if self.board.status == CODE_STALEMATE:
                    self.draws += 1
                    self.movesPerGame.append(movesGame)
                    self.board = Board()
                    break
                aiMove = bestMoveMinMax(self.board, self.board.getValidMoves(), depth, _time=120)
                # aiMove = MonteCarloTreeSearchNode(board=self.board, _depth_rollout=4, _time=0, _sim=simulations).best_move()
                self.board.aiToBoard(aiMove)
                self.board.printBoard()
                self.printStatus()
                if self.board.status == CODE_CHECKMATE:
                    self.blackWins += 1
                    self.movesPerGame.append(movesGame)
                    self.board = Board()
                    break
                if self.board.status == CODE_STALEMATE:
                    self.draws += 1
                    self.movesPerGame.append(movesGame)
                    self.board = Board()
                    break


def main():
    test = Testing()
    test.testing(3, 4, 3000, 60)
    test.printStatistics()

def plot():
    """GM Judit Polgar (2686) - GM Veselin Topalov (2786)
    Ajedrez UNAM KO Mexico City MEX, 2010.11.21
    White to win"""
#    # x-coordinates of left sides of bars 
#     left = [1, 2, 3, 4, 5, 6]
    
#     # heights of bars
#     height = [6, 7, 4, 4, 4, 3]
    
#     # labels for bars
#     tick_label = list()
#     for sim in range(3000, 6000, 500):
#         tick_label.append(sim)
#     print(len(tick_label))

#     # tick_label = [3000, 'two', 'three', 'four', 'five']
    
#     # plotting a bar chart
#     plt.bar(left, height, tick_label = tick_label,
#             width = 0.8, color = ['red', 'green'])
    
#     # naming the x-axis
#     plt.xlabel('Numar de simulări')
#     # naming the y-axis
#     plt.ylabel('Mutări necesare')
#     # plot title
#     plt.title('"""GM Judit Polgar (2686) - GM Veselin Topalov (2786)')
    
#     # function to show the plot
#     plt.show()
# frequencies
# setting the x - coordinates
    x = range(3000, 6000, 500)
    y = [6, 7, 4, 4, 4, 3]
    # setting the corresponding y - coordinates
    plt.xlabel('Numar de simulări')
    plt.ylabel('Mutări necesare pentru şah mat')
    # plotting the points
    plt.plot(x, y)
    
    # function to show the plot
    plt.show()
if __name__ == "__main__":
    main()
    # plot()
        
        
