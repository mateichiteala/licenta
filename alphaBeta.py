import sys
import time
import random
from typing import List

from ai import AI
from board import Board
from pieces.move import Move
from transpositionTable import TranspositionTable
from scores.score import scoreMaterial

CHECKMATE = 1000000
STALEMATE = 0
INF = sys.maxsize

class AlphaBeta(AI):
    def __init__(self, board: Board, depth: int, time=0):
        self.transpTable = TranspositionTable()
        self.new_hashes = {}
        self.board = board
        self.depth = depth
        self.time = time
        self.nextMove = None
        self.validMoves = list()
        super().__init__()

    def bestMoveAlphaBeta(self):
        random.shuffle(self.validMoves)
        self.validMoves = self.board.getValidMoves()
        start_time = time.time()
        end_time = None
        if self.time != 0:
            end_time = start_time + self.time 
        
        self.alphabeta(self.validMoves, self.depth, self.board.playerTurn, -INF, INF, end_time)
        return self.nextMove

    def getBestMoveAI(self):
        return self.bestMoveAlphaBeta()
        
    def returnScoreFromHash(self, _depth, hash):
        if hash in self.transpTable.hashTable and self.transpTable.hashTable[hash]["depth"] >= _depth:
            return self.transpTable.hashTable[hash]["score"]
        else:
            return False

    def updateHashTable(self, hash, _depth, score):
        if hash not in self.transpTable.hashTable or self.transpTable.hashTable[hash]["depth"] < _depth:
            self.transpTable.hashTable[hash]={
                "score": score,
                "depth": _depth
            }
            self.new_hashes[hash]={
                "score": score,
                "depth": _depth
            }

    def updateDatabase(self):
        self.transpTable.updateHashTable(self.new_hashes)

    def alphabeta(self, validMoves: List[Move], depth: int, playerTurn: bool, alpha, beta, end_time):
        score = 0
        resp = self.board.status
        if resp == 3:
            return STALEMATE
        if resp == 2:
            return -CHECKMATE - depth if self.board.playerTurn else CHECKMATE + depth
        
        if depth == 0:
            hash = self.transpTable.computeHash(self.board.board)
            result = self.returnScoreFromHash(depth, hash)
            return result if result != False else scoreMaterial(self.board)
                
        if playerTurn:
            maxScore = -INF
            move:Move
            for move in validMoves:
                self.board.aiToBoard(move)
                hash = self.transpTable.computeHash(self.board.board)
                result = self.returnScoreFromHash(depth - 1, hash)
                if result != False:
                    score = result
                else:
                    nextMoves = self.board.getValidMoves()
                    score = self.alphabeta(nextMoves, depth -1, False, alpha, beta, end_time)
                
                if score > maxScore:
                    maxScore = score
                    if depth == self.depth:
                        self.nextMove = move
                            
                self.board.undoMove()  
                alpha = max([alpha, score])
                if beta <= alpha or (end_time != None and time.time() > end_time):
                    break
                self.updateHashTable(hash, depth-1, score)
            return maxScore
        else:
            minScore = INF
            move: Move
            for move in validMoves:
                self.board.aiToBoard(move)
                hash = self.transpTable.computeHash(self.board.board)
                result = self.returnScoreFromHash(depth-1, hash)
                if result != False:
                    score = result
                else:
                    nextMoves = self.board.getValidMoves()
                    score = self.alphabeta(nextMoves, depth-1, True, alpha, beta, end_time)

                if score < minScore:
                    minScore = score
                    if depth == self.depth:
                        self.nextMove = move

                self.board.undoMove()
                
                beta = min([beta, score])
                if beta <= alpha or (end_time != None and time.time() > end_time):
                    break
                else:
                    self.updateHashTable(hash, depth-1, score)

            return minScore