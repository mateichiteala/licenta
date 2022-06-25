from bcrypt import kdf
from scores.knightScore import knightInfluencedByPawns
import scores.matrix as matrix
import pawnScore
tables={
    "pw": matrix.PawnTableW,
    "Nw": matrix.KnightTableW,
    "Bw": matrix.BishopTableW,
    "Rw": matrix.RookTableW,
    "Qw": matrix.QueenTableW,
    "Kw": matrix.KingMW,
    "pb": matrix.PawnTableB,
    "Nb": matrix.KnightTableB,
    "Bb": matrix.BishopTableB,
    "Rb": matrix.RookTableB,
    "Qb": matrix.QueenTableB,
    "Kb": matrix.KingMB,

}
def scoreMaterial(board):
    countPawns = pawnScore.getCountPawns(board)
    score = 0
    for row in board:
        for square in row:
            if square !=0:
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
    return score