import scores.matrix as matrix

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
    score = 0
    for row in board:
        for square in row:
            if square !=0:
                team = "w" if square.team else "b"
                positionalScore = tables[square.type + team][square.row][square.col]
                if square.team:
                    score += square.value + positionalScore
                if square.team is False:
                    score -= (square.value + positionalScore)
    return score