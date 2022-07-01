import random
import pieces.move as mv
from pieces.move import Move
import numpy as np
from board import Board
from board import CODE_CHECKMATE, CODE_STALEMATE, CODE_NORMAL
from board import STALEMATE, CHECKMATE

from collections import defaultdict
from scores.score import scoreMaterial

MAX = CHECKMATE
MIN = -CHECKMATE 

class MonteCarloTreeSearchNode():
    def __init__(self, board: Board, parent=None) -> None:
        self.board: Board = board
        self.parent: MonteCarloTreeSearchNode = parent
        self.children = []
        self.number_of_visits = 1
        self.results = defaultdict(int)
        self.results[1] = 0
        self.results[-1] = 0
        self.playerTurn = True if self.board.playerTurn else False
        self.value = 0

        self.untried_moves = list()
        self.untried_moves = self.untried_actions()
        self.depth = 3
        self.moveMade = None

    def is_terminal_node(self):
        return self.is_game_over()

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_game_over(self):
        resp = self.board.status
        if resp in [CODE_CHECKMATE, CODE_STALEMATE]:
            return True

        return True if self.depth == 0 else False

            
    def game_result(self):
        resp = self.board.status
        if resp == CODE_STALEMATE:
            return STALEMATE
        if resp == CODE_CHECKMATE:
            return -CHECKMATE if self.board.playerTurn else CHECKMATE

        return scoreMaterial(self.board)
            
    
    def untried_actions(self):
        return self.board.getValidMoves()


    def expansion(self):
        move = self.untried_moves.pop()
        self.board.aiToBoard(move)

        child_node = MonteCarloTreeSearchNode(board=self.board,
                parent=self)

        child_node.moveMade = move
        child_node.playerTurn = not self.playerTurn
        
        self.children.append(child_node)
        
        return child_node
    

    def bestChildWithdScore(self):

        return_value = MIN if self.playerTurn else MAX
        return_child = 0
        child: MonteCarloTreeSearchNode

        for child in self.children:
            if (return_value < child.value) == self.playerTurn:
                return_value = child.value
                return_child = child
            
        return return_child
            

    def best_child(self, C=2):
        choices_weights = list()
        child: MonteCarloTreeSearchNode
        for child in self.children:
            v = self.value
            N = self.number_of_visits 
            n = child.number_of_visits
            ucb = v + C * np.sqrt(np.log(N)/n)
            choices_weights.append(ucb)
        return self.children[np.argmax(choices_weights)]

    def selection(self):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expansion()
            else:
                current_node: MonteCarloTreeSearchNode = current_node.best_child()
                self.board.aiToBoard(current_node.moveMade)

        return current_node

    def simulation(self):
        count_moves = 0
        while not self.is_game_over():
            possible_moves = self.board.getValidMoves()
            move: Move = random.choice(possible_moves)
            self.board.aiToBoard(move)
            
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
        self.value += result
        if self.parent != None:
            self.board.undoMove()
            self.parent.backpropagation(result)


    def best_move(self):
        repeats = 10000
        for i in range(repeats):
            print(i)
            node = self.selection()
            result = node.simulation()
            node.backpropagation(result)


        best_child: MonteCarloTreeSearchNode = self.bestChildWithdScore()
        return best_child.moveMade


if __name__ == "__main__":
    pass