from copy import deepcopy
import random
from typing import List
from board import Board
from pieces.move import Move

from pieces.piece import Piece
from zobrist import ZobristClass
import scores
from scores.score import scoreMaterial
CHECKMATE = 1000
STALEMATE = 0
global nextMove
global new_hashes
global moves
global undoes
global index_nextMove



# knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
#                 [1, 2, 2, 2, 2, 2, 2, 1],
#                 [1, 2, 3, 3, 3, 3, 2, 1],
#                 [1, 2, 3, 4, 4, 3, 2, 1],
#                 [1, 2, 3, 4, 4, 3, 2, 1],
#                 [1, 2, 3, 3, 3, 3, 2, 1],
#                 [1, 2, 2, 2, 2, 2, 2, 1],
#                 [1, 1, 1, 1, 1, 1, 1, 1]
#             ]

# piecePositonScores = {"N": knightScores}
def findRandomMoves(validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]

def findBestMove(board: Board, validMoves: List[Move]):
    turnMultiplier = 1 if board.playerTurn else -1
    opponentMinMaxScore = CHECKMATE
    bestMove = None

    random.shuffle(validMoves)
    playerMove: Move
    for playerMove in validMoves:
        # Make move
        board.move(playerMove)

        opponentMaxScore = -CHECKMATE
        # Change Turn
        playerTurn = not board.playerTurn
        
        # All opponet's moves
        opponentMoves = board.allValidMoves(playerTurn)
        opponentMove: Move
        for opponentMove in opponentMoves:
            # Make the opponent move
            board.move(opponentMove)
            validMoves, check, _ = board.isCheck(playerTurn)
            
            if check and len(validMoves) == 0:
                score = -turnMultiplier * CHECKMATE
            elif board.isStalemate(playerTurn):
                score = STALEMATE
            else:
                score = -turnMultiplier * scoreMaterial(board.board)
            # Take the opponent's best move
            if score > opponentMaxScore:
                opponentMaxScore = score
            board.undoMove()

        # Get the move with opponet's lowest score
        if opponentMaxScore < opponentMinMaxScore:
            opponentMinMaxScore = opponentMaxScore
            bestMove = playerMove
        board.undoMove()
        

    return bestMove

# def scoreMaterial(board: Board):
#     score = 0
#     for row in board:
#         square: Piece
#         for square in row:
#             if square != 0 and square.team:
#                 score += square.value
#             if square != 0 and square.team is False:
#                 score -= square.value
#     return score

DEPTH = 4
zob = ZobristClass()
import time
def minimax_timeout(board, validMoves, DEPTH, playerTurn):
    minimax(board, validMoves, DEPTH, playerTurn, -CHECKMATE, CHECKMATE)


def bestMoveMinMax(board: Board, validMoves: List[Move]):
    global nextMove
    global new_hashes
    global moves
    global undoes
    global index_nextMove

    nextMove = None
    new_hashes = {}
    moves = 0
    undoes = 0
    index_nextMove = 0

    random.shuffle(validMoves)
    start_time = time.time()
    end_time = start_time + 60*6
    print("alpha-beta")
    minimax(board, validMoves, DEPTH, board.playerTurn, -CHECKMATE, CHECKMATE, end_time)
    zob.updateHashTable(new_hashes)
    return nextMove


def minimax(board: Board, validMoves: List[Move], depth: int, playerTurn: bool, alpha, beta, end_time):
    global nextMove
    global new_hashes
    global moves
    global undoes
    global index_nextMove
    index_nextMove = 0

    resp = board.statusBoard()
    if resp == 2:
        return 5000 if board.playerTurn else -5000

    if depth == 0:
        hash = zob.computeHash(board.board)
        if hash not in zob.hashTable:
            return scoreMaterial(board.board)
        else:
            return zob.hashTable[hash]["score"]

    if playerTurn:
        maxScore = -CHECKMATE
        move:Move
        for index, move in enumerate(validMoves):
            board.move(move)
            hash = zob.computeHash(board.board)
            # if hash not in zob.hashTable or zob.hashTable[hash]["depth"] < depth-1:

            if hash in zob.hashTable and zob.hashTable[hash]["depth"] > depth:
                score = zob.hashTable[hash]["score"]
            else:
                nextMoves = board.allValidMoves(False)
                score = minimax(board, nextMoves, depth-1, False, alpha, beta, end_time)

            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
                    index_nextMove = index
                        
            board.undoMove()  

            alpha = max([alpha, score])
            if beta <= alpha or time.time() > end_time:
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
        minScore = CHECKMATE
        move: Move
        for index, move in enumerate(validMoves):
            board.move(move)

            hash = zob.computeHash(board.board)
            if hash in zob.hashTable and zob.hashTable[hash]["depth"] > depth-1:
                score = zob.hashTable[hash]["score"]
            else:
                nextMoves = board.allValidMoves(True)
                score = minimax(board, nextMoves, depth-1, True, alpha, beta, end_time)
                
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
                    index_nextMove = index
                
            
            board.undoMove()
            
            beta = min([beta, score])
            if beta <= alpha or time.time() > end_time:
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