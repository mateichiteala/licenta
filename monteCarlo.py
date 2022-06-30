import random
import pieces.move as mv
from pieces.move import Move
import numpy as np
from board import Board
from collections import defaultdict
from scores.score import scoreMaterial


class MonteCarloTreeSearchNode():
    def __init__(self, board: Board, parent=None) -> None:
        self.board: Board = board
        self.parent: MonteCarloTreeSearchNode = parent
        self.children = []
        self.number_of_visits = 1
        self.results = defaultdict(int)
        self.results[1] = 0
        self.results[-1] = 0
        self.untried_moves = self.untried_actions()
        self.depth = 6
        self.playerTurn = True if self.board.playerTurn is True else False
        self.moveMade = None

    def is_terminal_node(self):
        return self.is_game_over()

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_game_over(self):
        # 1
        resp = self.board.statusBoard()
        if resp == 2:
            return True
        if resp == 3:
            print("sal")
            return True

        # 2 
        resp = self.board.statusBoard(not self.playerTurn)
        if resp == 2:
            return True
        if resp == 3:
            return True
        if self.depth == 0:
            return True
        else:
            return False
            
    def game_result(self):
        resp = self.board.statusBoard()
        if resp == 1:
            return 1 if self.board.playerTurn else -1
        if resp == 2:
            return 1 if self.board.playerTurn else -1
        if resp == 3:
            return 0

        score = scoreMaterial(self.board)
        if score == 0:
            return 0
        return 1 if score > 0 else -1
            
    
    def untried_actions(self):
        self.untried_moves = self.board.allValidMoves(self.board.playerTurn)
        return self.untried_moves


    def expansion(self):
        move = self.untried_moves.pop()
        self.board.move(move)

        child_node = MonteCarloTreeSearchNode(board=self.board,
                parent=self)
        child_node.moveMade = move
        child_node.depth = self.depth -1
        child_node.playerTurn = not self.playerTurn
        self.children.append(child_node)
        
        return child_node
    

    def mostSimulationsChild(self):
        max_visits = 0
        max_child = 0
        child: MonteCarloTreeSearchNode
        for child in self.children:
            if max_visits < child.number_of_visits:
                max_visits = child.number_of_visits
                max_child = child
        
        return max_child

    def best_child(self, C=0.1):
        choices_weights = list()
        child: MonteCarloTreeSearchNode
        team = 1 if self.playerTurn else -1 
        for child in self.children:
            v = team * (child.results[1] - child.results[-1]) / child.number_of_visits # white - black / number_of_visits
            value = v + C * np.sqrt(self.number_of_visits / child.number_of_visits)
            choices_weights.append(value)
        return self.children[np.argmax(choices_weights)]

    def selection(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expansion()
            else:
                current_node: MonteCarloTreeSearchNode = current_node.best_child()
                self.board.move(current_node.moveMade)

        return current_node

    def simulation(self):
        count_moves = 0
        while not self.is_game_over():
            possible_moves = self.board.allValidMoves(self.board.playerTurn)
            if len(possible_moves) == 0:
                self.board.printBoard()
            move: Move = random.choice(possible_moves)
            self.board.move(move)
            self.depth -= 1
            count_moves += 1
        
        result = self.game_result() 
        while count_moves > 0:
            self.board.undoMove()
            count_moves -= 1
            self.depth += 1
        

        return result

    def backpropagation(self, result):
        self.number_of_visits += 1
        self.results[result] += 1
        if self.parent != None:
            self.board.undoMove()
            self.parent.backpropagation(result)

    def best_move(self):
        repeats = 1500
        aux = self.depth
        for i in range(repeats):
            print(i)
            self.depth = aux
            node = self.selection()
            result = node.simulation()
            node.backpropagation(result)


        best_child: MonteCarloTreeSearchNode = self.mostSimulationsChild()
        return best_child.moveMade


# def scoreMaterial(board):
#         score = 0
#         for row in board:
#             square: Piece
#             for square in row:
#                 if square != 0 and square.team:
#                     score += square.value
#                 if square != 0 and square.team is False:
#                     score -= square.value
#         return score


def main():
    initial_board = Board()
    print(mv.fromPNGtoMove("O-O", initial_board))
    import random
    with open('Games.txt') as f:
        lines = [line.rstrip() for line in f]
        
    print(lines[0].split()[0])
    # root = MonteCarloTreeSearchNode(board = initial_board)
    # moveMade: Move = root.best_move()
    
    # initial_board.move(moveMade)
    # print(moveMade.get())
    # print(moveMade.getChessNotation())
    # # 2
    # # root = MonteCarloTreeSearchNode(board = initial_board)
    # # moveMade: Move = root.best_move()

    # # initial_board.move(moveMade)
    # # print(moveMade.get())
    # # initial_board.printBoard()





if __name__ == "__main__":
    main()