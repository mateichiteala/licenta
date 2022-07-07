import random
import time
import numpy as np
from ai import AI
from alphaBeta import INF

from pieces.move import Move
from board import CODE_CHECK, Board
from board import CODE_CHECKMATE, CODE_STALEMATE
from board import STALEMATE, CHECKMATE, CHECK
from scores.score import scoreMaterial

MAX = CHECKMATE
MIN = -CHECKMATE 

class MonteCarloTreeSearchNode(AI):
    def __init__(self, board: Board, parent=None, _time=0, _depth_rollout=6, _sim=1000) -> None:
        self.board: Board = board
        self.parent: MonteCarloTreeSearchNode = parent
        self.children = []
        self.number_of_visits = 1
        self.playerTurn = True if self.board.playerTurn else False
        self.value = 0
        self.time = _time
        self.untried_moves = list()
        self.untried_moves = self.untried_actions()
        self.depth_rollout = _depth_rollout
        self.depth_node = 0
        self.sim = _sim
        self.moveMade = None
        super().__init__()

    def setPlayerTurn(self):
        self.playerTurn = True if self.board.playerTurn else False

    def is_terminal_node(self):
        return self.is_game_over()

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def is_game_over(self):
        resp = self.board.status
        if resp in [CODE_CHECKMATE, CODE_STALEMATE]:
            return True

        return True if self.depth_rollout == 0 else False

            
    def game_result(self):
        resp = self.board.status
        if resp == CODE_STALEMATE:
            return STALEMATE
        if resp == CODE_CHECKMATE:
            return -CHECKMATE +  self.depth_node*10 if self.board.playerTurn else CHECKMATE - self.depth_node*10
        
        return scoreMaterial(self.board)
            
    def untried_actions(self):
        return self.board.getValidMoves()


    def expansion(self):
        move = self.untried_moves.pop()
        self.board.aiToBoard(move)

        child_node = MonteCarloTreeSearchNode(board=self.board,
                parent=self)
        child_node.depth_node = self.depth_node + 1
        child_node.moveMade = move
        child_node.playerTurn = not self.playerTurn
        
        self.children.append(child_node)
        
        return child_node
    

    def bestChildWithdScore(self):
        return_value = -INF if self.playerTurn else INF
        return_child = random.choice(self.children)
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
            n = self.number_of_visits 
            ni = child.number_of_visits
            v = self.value
            v /= ni

            ucb = v + C * np.sqrt(np.log(n)/ni)
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
            
            self.depth_rollout -= 1
            count_moves += 1
 
        result = self.game_result() 
        while count_moves > 0:
            self.board.undoMove()
            count_moves -= 1
            self.depth_rollout += 1
        
        return result

    def backpropagation(self, result):
        self.number_of_visits += 1
        self.value += result
        if self.parent != None:
            self.board.undoMove()
            self.parent.backpropagation(result)

    def setUntriedMoves(self):
        self.untried_moves = self.board.getValidMoves()

    def getBestMoveAI(self):
        self.setPlayerTurn()
        self.setUntriedMoves()
        self.parent = None

        if len(self.children) > 0:
            self = MonteCarloTreeSearchNode(board=self.board, _time=self.time, _sim=self.sim, parent=None)
        start_time = time.time()
        end_time = None
        if self.time != 0:
            end_time = start_time + self.time
        
        for i in range(self.sim):
            # print(i)
            if end_time != None and time.time() > end_time:
                break
            node = self.selection()
            result = node.simulation()
            node.backpropagation(result)

        best_child: MonteCarloTreeSearchNode = self.bestChildWithdScore()
        return best_child.moveMade

# class MonteCarloTreeSearchNode(AI):
#     def __init__(self, board: Board, parent=None, _time=0,  _sim=1000) -> None:
#         self.board: Board = board
#         self.parent: MonteCarloTreeSearchNode = parent
#         self.children = []
#         self.number_of_visits = 1
#         self.playerTurn = True if self.board.playerTurn else False
#         self.result = dict()
#         self.result[-1] = 0
#         self.result[1] = 0
#         self.result[0] = 0

#         self.time = _time
#         self.untried_moves = list()
#         self.untried_moves = self.untried_actions()
#         self.sim = _sim
#         self.moveMade = None
#         super().__init__()

#     def is_terminal_node(self):
#         return self.is_game_over()

#     def is_fully_expanded(self):
#         return len(self.untried_moves) == 0

#     def is_game_over(self):
#         resp = self.board.status
#         if resp in [CODE_CHECKMATE, CODE_STALEMATE]:
#             return True
       
#     def game_result(self):
#         resp = self.board.status
#         if resp == CODE_STALEMATE:
#             return 0
#         if resp == CODE_CHECKMATE:
#             return -1 if self.board.playerTurn else 1
                    
#     def untried_actions(self):
#         return self.board.getValidMoves()


#     def expansion(self):
#         move = self.untried_moves.pop()
#         self.board.aiToBoard(move)

#         child_node = MonteCarloTreeSearchNode(board=self.board,
#                 parent=self)
#         child_node.moveMade = move
#         child_node.playerTurn = not self.playerTurn
        
#         self.children.append(child_node)
        
#         return child_node
    
#     def updateTree(self, move: Move):
#         child: MonteCarloTreeSearchNode
#         for child in self.children:
#             if move == child.moveMade:
#                 self = child
#                 return
#         self = MonteCarloTreeSearchNode(board=self.board, _time=self.time, _sim=self.sim, parent=None)

#     def bestChildWithRepetition(self):
#         return_child: MonteCarloTreeSearchNode = random.choice(self.children)
#         return_repetition = return_child.number_of_visits
#         child: MonteCarloTreeSearchNode

#         for child in self.children:
#             if return_repetition < child.number_of_visits:
#                 return_repetition = child.number_of_visits
#                 return_child = child
            
#         return return_child
            
#     def best_child(self, C=2):
#         choices_weights = list()
#         child: MonteCarloTreeSearchNode
#         for child in self.children:
#             ni = child.number_of_visits
#             n = self.number_of_visits 

#             v = child.result[1] if child.playerTurn else child.result[-1]
#             v /=  ni
            
#             ucb = v + C * np.sqrt(np.log(n)/ni)
#             choices_weights.append(ucb)
#         return self.children[np.argmax(choices_weights)]

#     def selection(self):
#         current_node = self
#         while not current_node.is_terminal_node():
#             if not current_node.is_fully_expanded():
#                 return current_node.expansion()
#             else:
#                 current_node: MonteCarloTreeSearchNode = current_node.best_child()
#                 self.board.aiToBoard(current_node.moveMade)
#         return current_node

#     def simulation(self):
#         count_moves = 0
#         while not self.is_game_over():
#             possible_moves = self.board.getValidMoves()
#             move: Move = random.choice(possible_moves)
#             self.board.aiToBoard(move)
#             count_moves += 1
 
#         result = self.game_result() 
#         while count_moves > 0:
#             self.board.undoMove()
#             count_moves -= 1
        
#         return result

#     def backpropagation(self, result):
#         self.number_of_visits += 1
#         self.result[result] += result
#         if self.parent != None:
#             self.board.undoMove()
#             self.parent.backpropagation(result)


#     def getBestMoveAI(self):
#         if len(self.children) > 0:
#             self = MonteCarloTreeSearchNode(board=self.board, _time=self.time, _sim=self.sim, parent=None)
#         start_time = time.time()
#         end_time = None
#         if self.time != 0:
#             end_time = start_time + self.time
        
#         for i in range(self.sim):
#             print(i)
#             if end_time != None and time.time() > end_time:
#                 break
#             node = self.selection()
#             result = node.simulation()
#             node.backpropagation(result)

#         best_child: MonteCarloTreeSearchNode = self.bestChildWithRepetition()

#         self = best_child
#         return best_child.moveMade





if __name__ == "__main__":
    pass