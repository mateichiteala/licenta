import time
import random
import sys
from typing import List

from board import Board
from pieces.move import Move
from zobrist import TranspositionTable
from scores.score import scoreMaterial

CHECKMATE = 1000000
STALEMATE = 0
INF = sys.maxsize
global nextMove
global new_hashes
global moves
global undoes
global DEPTH


zob = TranspositionTable()

def bestMoveMinMax(board: Board, validMoves: List[Move], depth, _time):
    global nextMove
    global new_hashes
    global moves
    global undoes
    global DEPTH

    nextMove = None
    new_hashes = {}
    moves = 0
    undoes = 0
    DEPTH = depth

    random.shuffle(validMoves)

    start_time = time.time()
    end_time = None
    if _time != 0:
        end_time = start_time + _time
    
    transp_time_start = time.time()
    minimax(board, validMoves, DEPTH, board.playerTurn, -INF, INF, end_time)
    transp_time_end = time.time()
    print(transp_time_end - transp_time_start)
    
    zob.updateHashTable(new_hashes)
    
    return nextMove


def minimax(board: Board, validMoves: List[Move], depth: int, playerTurn: bool, alpha, beta, end_time):
    global nextMove
    global new_hashes
    global moves
    global undoes

    score = 0
    resp = board.status
    if resp == 3:
        return STALEMATE
    if resp == 2:
        return -CHECKMATE - depth if board.playerTurn else CHECKMATE + depth
    
    if depth == 0:
        hash = zob.computeHash(board.board)
        if hash not in zob.hashTable:
            return scoreMaterial(board) + score
        else:
            return zob.hashTable[hash]["score"]

    if playerTurn:
        maxScore = -INF
        move:Move
        for move in validMoves:
            board.aiToBoard(move)
            hash = zob.computeHash(board.board)
            if hash in zob.hashTable and zob.hashTable[hash]["depth"] > depth:
                score = zob.hashTable[hash]["score"]
            else:
                nextMoves = board.getValidMoves()
                score = minimax(board, nextMoves, depth-1, False, alpha, beta, end_time)
            
            # better value
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
                        
            board.undoMove()  
            # if 
            alpha = max([alpha, score])
            if beta <= alpha or (end_time != None and time.time() > end_time):
                break
            else:
                if hash not in zob.hashTable or zob.hashTable[hash]["depth"] < depth:
                    zob.hashTable[hash]={
                        "score": score,
                        "depth": depth
                    }
                    new_hashes[hash]={
                        "score": score,
                        "depth": depth
                    }
        return maxScore
    else:
        minScore = INF
        move: Move
        for move in validMoves:
            board.aiToBoard(move)
            hash = zob.computeHash(board.board)
            if hash in zob.hashTable and zob.hashTable[hash]["depth"] > depth-1:
                score = zob.hashTable[hash]["score"]
            else:
                nextMoves = board.getValidMoves()
                score = minimax(board, nextMoves, depth-1, True, alpha, beta, end_time)
            

            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move

            board.undoMove()
            
            beta = min([beta, score])
            if beta <= alpha or (end_time != None and time.time() > end_time):
                break
            else:
                if hash not in zob.hashTable or zob.hashTable[hash]["depth"] < depth-1:
                    zob.hashTable[hash]={
                        "score": score,
                        "depth": depth-1
                    }
                    new_hashes[hash]={
                        "score": score,
                        "depth": depth-1
                    }

        return minScore