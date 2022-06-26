import random
from ai import DEPTH
import pieces.move as mv
from pieces.move import Move
from pieces.piece import Piece
import numpy as np
from board import Board
from collections import defaultdict
from scores.score import scoreMaterial
# DEPTH = 2
# class MonteCarloTreeSearchNode():
#     def __init__(self, board, parent=None, parent_action=None, depth = 2):
#         self.original_board: Board = board
#         self.board: Board = board # board
#         self.parent: MonteCarloTreeSearchNode = parent
#         self.parent_action = parent_action
#         self.children = []
#         self._number_of_visits = 0
#         self._results = defaultdict(int)
#         self._results[1] = 0
#         self._results[-1] = 0
#         self._untried_actions = None
#         self._untried_actions = self.untried_actions()
#         self.depth = depth
#         self.playerTurn = self.board.playerTurn

#         return

#     def untried_actions(self):
#         self._untried_actions = self.board.allValidMoves(self.board.playerTurn)
#         return self._untried_actions

#     def q(self):
#         wins = self._results[1]
#         loses = self._results[-1]
#         return wins - loses

#     def n(self):
#         return self._number_of_visits

#     def expand(self):
#         action = self._untried_actions.pop()
#         self.board.move(action)
#         print("MOVE")

#         next_board = self.board

#         child_node = MonteCarloTreeSearchNode(
#             next_board, parent=self, parent_action=action)
#         self.children.append(child_node)

#         return child_node
    
#     def is_terminal_node(self):
#         return self.is_game_over()

#     def rollout(self):
#         current_rollout_board = self.board
#         while not self.is_game_over():
#             possible_moves = current_rollout_board.allValidMoves(self.board.playerTurn)
#             action = self.rollout_policy(possible_moves)
#             current_rollout_board.move(action)

#         return self.game_result()

#     def backpropagate(self, result):
#         self._number_of_visits += 1.
#         self._results[result] += 1.
#         if self.parent != None:
#             self.parent.backpropagate(result)

#     def is_fully_expanded(self):
#         return len(self._untried_actions) == 0

#     def best_child(self, c_param=0.1):
#         choices_weights = [(c.q() / c.n()) + c_param * np.sqrt((2 * np.log(self.n()) / c.n())) for c in self.children]
#         return self.children[np.argmax(choices_weights)]

#     def rollout_policy(self, possible_moves):
#         return possible_moves[np.random.randint(len(possible_moves))]

#     def _tree_policy(self):
#         current_node = self
#         while not current_node.is_terminal_node():
#             if not current_node.is_fully_expanded():
#                 return current_node.expand()
#             else:
#                 current_node = current_node.best_child()
#         return current_node

#     def best_action(self):
#         simulation_no = 200
#         for _ in range(simulation_no):
#             v = self._tree_policy()
#             reward = v.rollout()
#             v.backpropagate(reward)
#             self.board = self.original_board
        
#         return self.best_child(c_param=0.)


#     def is_game_over(self):
#         if self.depth == 0:
#             return True
#         else:
#             self.depth -= 1
#             return self.board.checkMate()
            
#     def game_result(self):
#         '''
#         Modify according to your game or 
#         needs. Returns 1 or 0 or -1 depending
#         on your board corresponding to win,
#         tie or a loss.
#         '''
#         score = scoreMaterial(self.board.board)
#         if score > 0:
#             return 0
#         if self.playerTurn:
#             return 1 if score > 0 else -1
#         else:
#             return 1 if score < 0 else -1
            
# def scoreMaterial(board):
#     # validMoves, check, _ =board.isCheck(board.playerTurn)
#     # if check and len(validMoves) == 0:
#     #     if board.playerTurn:
#     #         return -CHECKMATE
#     #     else:
#     #         return CHECKMATE
#     # elif board.isStalemate(board.playerTurn):
#     #     return STALEMATE

#     score = 0
#     for row in board:
#         square: Piece
#         for square in row:
#             if square != 0 and square.team:
#                 score += square.value
#             if square != 0 and square.team is False:
#                 score -= square.value
#     return score



# def main():
#     initial_board = Board()
#     root = MonteCarloTreeSearchNode(board = initial_board)
#     selected_node = root.best_action()
#     selected_node.board.printBoard()
#     return 

# if __name__ == "__main__":
#     main()

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
        if self.depth == 0:
            return True
            
    def game_result(self):
        score = scoreMaterial(self.board.board)
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
        repeats = 10000
        aux = self.depth
        for _ in range(repeats):
            self.depth = aux
            node = self.selection()
            result = node.simulation()
            node.backpropagation(result)


        best_child: MonteCarloTreeSearchNode = self.best_child()
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