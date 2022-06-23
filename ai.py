from copy import copy
from multiprocessing import Queue
import random
from typing import List
from board import Board
from pieces.move import Move

from pieces.piece import Piece
from zobrist import ZobristClass

CHECKMATE = 1000
STALEMATE = 0
global nextMove
global new_hashes


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

def scoreMaterial(board: Board):
    # validMoves, check, _ =board.isCheck(board.playerTurn)
    # if check and len(validMoves) == 0:
    #     if board.playerTurn:
    #         return -CHECKMATE
    #     else:
    #         return CHECKMATE
    # elif board.isStalemate(board.playerTurn):
    #     return STALEMATE

    score = 0
    for row in board:
        square: Piece
        for square in row:
            piecePositionScore = 0
            if square != 0 and square.team:
                score += square.value
            if square != 0 and square.team is False:
                score -= square.value
    return score

DEPTH = 3
zob = ZobristClass()

def bestMoveMinMax(board: Board, validMoves: List[Move]):
    global nextMove
    global new_hashes
    nextMove = None
    new_hashes = {}

    random.shuffle(validMoves)
    minimax(board, validMoves, DEPTH, board.playerTurn, -CHECKMATE, CHECKMATE)
    
    zob.updateHashTable(new_hashes)
    
    return nextMove


def minimax(board: Board, validMoves: List[Move], depth: int, playerTurn: bool, alpha, beta):
    global nextMove
    global new_hashes

    if depth == 0:
        hash = zob.computeHash(board.board)
        if hash in zob.hashTable:
            return zob.hashTable[hash]
        else:
            print(hash)
            val = scoreMaterial(board.board)
            zob.hashTable[hash] = val
            new_hashes[hash] = val
            return val
        # return scoreMaterial(board.board)

    if playerTurn:
        maxScore = -CHECKMATE
        move:Move
        for move in validMoves:
            board.move(move)
            nextMoves = board.allValidMoves(False)
            score = minimax(board, nextMoves, depth-1, False, alpha, beta)
            board.undoMove()            
            
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
                    
            alpha = max([alpha, score])
            if beta <= alpha:
                break
        return maxScore
    else:
        minScore = CHECKMATE
        move: Move
        for move in validMoves:
            board.move(move)
            nextMoves = board.allValidMoves(True)
            score = minimax(board, nextMoves, depth-1, True, alpha, beta)
            board.undoMove()
            
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move

            beta = min([beta, score])
            if beta <= alpha:
                break

        return minScore