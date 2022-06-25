def bishopPair(board):
    score = {
        True: 0,
        False: 0
    }
    for row in board:
        for square in row:
            if square !=0 and square.type == "B":
               score[square.team] += 1

    for key, value in score:
        score[key] = 50 if value > 1 else 0
    
    return score

        