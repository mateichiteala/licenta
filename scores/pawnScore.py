import numpy as np

def doubledPawmScore(board):
    transpose_board = np.transpose(board)
    score = {
        True: 0,
        False: 0
    }
    for col in transpose_board:
        for square in col:
            count_pawns = {
                True: 0,
                False: 0
            }
            if square !=0 and square.type == "p":
                count_pawns[square.team] += 1
        for key, value in count_pawns:
            count_pawns[key] *= 25 if value > 1 else 0
            score[key] += count_pawns[key]

    return score

def isolatedPawn(board):
    score = {
        True: 0,
        False: 0
    }
    for i, row in enumerate(board):
        for j, square in enumerate(row):
            isolated = True
            if square !=0 and square.type == "p":
                for directionX in [-1, 1]:
                    if 0 <= j + directionX <=7 and board[i][j + directionX].type == "p" and board[i][j + directionX].team == square.team:
                        isolated = False
                        break
                    for directionY in [-1, 1]:
                        if 0 <= i + directionY <=7 and board[i + directionY][j].type == "p" and board[i][j + directionX].team == square.team:
                            isolated = False
                            break
                if isolated:
                    score[square.team] += 1
    for key in score:
        score[key] *= 15
        
    return score


def getCountPawns(board):
    score = {
        True: 0,
        False: 0
    }

    for row in board:
        for square in row:
            if square !=0 and square.type == "p":
                score[square.team] += 1

    return score
                            

                    


