import numpy as np

def rookOpenFile(board):
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