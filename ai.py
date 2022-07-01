from copy import deepcopy
import random
from typing import List
from board import Board
from pieces.move import Move

from pieces.piece import Piece
from pieces.rook import Rook
from zobrist import ZobristClass
import scores
from scores.score import scoreMaterial
CHECKMATE = 1000000
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

DEPTH = 6
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

    score = 0
    
    resp = board.status
    if resp == 3:
        return STALEMATE
    if resp == 2:
        return CHECKMATE if board.playerTurn else -CHECKMATE
    if resp == 1:
        score += -200 if board.playerTurn else 200
    
    if depth == 0:
        hash = zob.computeHash(board.board)
        if hash not in zob.hashTable:
            return scoreMaterial(board) + score
        else:
            return zob.hashTable[hash]["score"]

    if playerTurn:
        maxScore = -CHECKMATE
        move:Move
        for index, move in enumerate(validMoves):
            board.aiToBoard(move)
            
            hash = zob.computeHash(board.board)
            # if hash not in zob.hashTable or zob.hashTable[hash]["depth"] < depth-1:
            if hash in zob.hashTable and zob.hashTable[hash]["depth"] > depth:
                score = zob.hashTable[hash]["score"]
            else:
                nextMoves = board.getValidMoves()
                score = minimax(board, nextMoves, depth-1, False, alpha, beta, end_time)
            
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
                        
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

            board.aiToBoard(move)

            hash = zob.computeHash(board.board)
            if hash in zob.hashTable and zob.hashTable[hash]["depth"] > depth-1:
                score = zob.hashTable[hash]["score"]
            else:
                
                # nextMoves = board.allValidMoves(True, pins, attackPins)
                nextMoves = board.getValidMoves()
                score = minimax(board, nextMoves, depth-1, True, alpha, beta, end_time)
                
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move

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