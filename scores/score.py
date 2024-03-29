import scores.matrix as matrix
from board import CODE_CHECK
from scores.pawnScore import doubledPawnScore, getCountPawns, isolatedPawn
from scores.bishopScore import bishopPair
from scores.rookScore import rookOpenFile

tables={
    "pw": matrix.PawnTableW,
    "Nw": matrix.KnightTableW,
    "Bw": matrix.BishopTableW,
    "Rw": matrix.RookTableW,
    "Qw": matrix.QueenTableW,
    "Kwm": matrix.KingMW,
    "pb": matrix.PawnTableB,
    "Nb": matrix.KnightTableB,
    "Bb": matrix.BishopTableB,
    "Rb": matrix.RookTableB,
    "Qb": matrix.QueenTableB,
    "Kbm": matrix.KingMB,
    "Kb": matrix.KingEB,
    "Kw": matrix.KingEW
}

def scoreMaterial(_board):
    board = _board.board
    countPawns = getCountPawns(board)
    score = 0
    for row in board:
        for square in row:
            if square !=0:
                _knightInfluencedByPawnsScore = 0
                _rookInfluencedByPawnsScore = 0
                team = "w" if square.team else "b"
                positionalScore = tables[square.type + team][square.row][square.col]
                if square.type == "N":
                    _knightInfluencedByPawnsScore =  (countPawns[not square.team] - 8) * 10
                if square.type == "R":
                    _rookInfluencedByPawnsScore =  (8 - countPawns[not square.team]) * 10 
                    
                if square.team:
                    score += square.value + positionalScore + _knightInfluencedByPawnsScore  + _rookInfluencedByPawnsScore
                if square.team is False:
                    score -= (square.value + positionalScore + _knightInfluencedByPawnsScore + _rookInfluencedByPawnsScore)

    score += bishopPair(board)
    score += rookOpenFile(board)
    score += doubledPawnScore(board)
    score += isolatedPawn(board)

    if _board.status == CODE_CHECK:
        score += -100 if _board.playerTurn else 100
    
    return score