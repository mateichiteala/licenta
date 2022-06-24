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

DEPTH = 3
zob = ZobristClass()
import func_timeout

def minimax_timeout(board, validMoves, DEPTH, playerTurn):
    minimax(board, validMoves, DEPTH, playerTurn, -CHECKMATE, CHECKMATE)


def bestMoveMinMax(board: Board, validMoves: List[Move]):
    global nextMove
    global new_hashes
    global moves
    global undoes
    nextMove = None
    new_hashes = {}
    moves = 0
    undoes = 0

    random.shuffle(validMoves)
    # board.unloadImages()
    # board_copy = deepcopy(board)
    # board.reloadImages()
    try:
       return func_timeout.func_timeout(60, minimax_timeout, args=[board, validMoves, DEPTH, board.playerTurn])
    except func_timeout.FunctionTimedOut as e:
        print("Nu a fost gata in 60s!")
        while moves - undoes :
            moves -= 1
            print("undo")
            board.undoMove()

    # minimax(board, validMoves, DEPTH, board.playerTurn, -CHECKMATE, CHECKMATE)
    zob.updateHashTable(new_hashes)
    
    return nextMove


def minimax(board: Board, validMoves: List[Move], depth: int, playerTurn: bool, alpha, beta):
    global nextMove
    global new_hashes
    global moves
    global undoes

    if depth == 0:
        hash = zob.computeHash(board.board)
        if hash not in zob.hashTable:
            return scoreMaterial(board.board)
        else:
            return zob.hashTable[hash]["score"]

    if playerTurn:
        maxScore = -CHECKMATE
        move:Move
        for move in validMoves:
            board.move(move)
            moves += 1
            hash = zob.computeHash(board.board)
            # if hash not in zob.hashTable or zob.hashTable[hash]["depth"] < depth-1:

            if hash in zob.hashTable and zob.hashTable[hash]["depth"] > depth:
                nextMove = move
                score = zob.hashTable[hash]["score"]
            else:
                nextMoves = board.allValidMoves(False)
                score = minimax(board, nextMoves, depth-1, False, alpha, beta)

                if score > maxScore:
                    maxScore = score
                    if depth == DEPTH:
                        nextMove = move
                        
            board.undoMove()  
            undoes += 1

            alpha = max([alpha, score])
            if beta <= alpha:
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
        for move in validMoves:
            board.move(move)
            moves += 1

            hash = zob.computeHash(board.board)
            if hash in zob.hashTable and zob.hashTable[hash]["depth"] > depth-1:
                nextMove = move
                score = zob.hashTable[hash]["score"]
            else:
                nextMoves = board.allValidMoves(True)
                score = minimax(board, nextMoves, depth-1, True, alpha, beta)
                
                if score < minScore:
                    minScore = score
                    if depth == DEPTH:
                        nextMove = move
                
            
            board.undoMove()
            undoes += 1
            
            beta = min([beta, score])
            if beta <= alpha:
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