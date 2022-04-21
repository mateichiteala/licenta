import pygame
from board import Board
from pieces.piece import Piece
from pieces.move import Move

WIDTH = 512
HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION

MAX_FPS = 15


def drawBoard(screen):
    colors = [pygame.Color("white"), pygame.Color("grey")]
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            color = colors[(row+col)%2]
            pygame.draw.rect(screen, color, pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawPieces(screen, board):
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            piece: Piece = board[row][col]
            if piece != 0:
                screen.blit(piece.getImage(), pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


def drawGameState(screen, board):
    drawBoard(screen)
    drawPieces(screen, board)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    board = Board()
    running = True
    square_selected = ()
    player_move = []
    i = 1
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:

                # Am I in check? Pins ? Valid moves ?
                validMoves, check, pins = board.isCheck(board.playerTurn)
                if check and len(validMoves) == 0:
                    print("CHECKMATE")
                # get position of mouse
                location = pygame.mouse.get_pos()
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE
                if len(player_move) == 0 and board.board[row][col] == 0:
                    continue
                if square_selected == (row, col):
                    square_selected = ()
                    player_move.clear()
                else:
                    square_selected = (row, col)
                    player_move.append(square_selected)
                    if len(player_move) == 2:
                        pieceMoved: Piece = board.board[player_move[0][0]][player_move[0][1]]
                        pieceCaptured = board.board[player_move[1][0]][player_move[1][1]]
                        move = Move(player_move[0], player_move[1], pieceMoved, pieceCaptured)
                        if pieceMoved.team == board.playerTurn:
                            if check:
                                print("check")
                                if move in validMoves:
                                    print(move.get())
                                    board.move(move)
                                else:
                                    print("not valid move")
                            else:
                                stalemate = board.isStalemate(board.playerTurn, pins)
                                i += 1
                                if i == 9:
                                    print("sal")
                                if stalemate:
                                    print("STALEMATE")
                                if pieceMoved not in pins:
                                    board.move(move)
                                    # stalemate ?
                                    # Am I in check after move
                                    validMoves, check, pins = board.isCheck(not board.playerTurn)
                                    if check:
                                        print("not a valid move")
                                        board.undoMove()
                        else:
                            print("Not your turn!")
                        square_selected = ()
                        board.printBoard()
                        player_move.clear()
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    board.undoMove()
                    square_selected = ()
                    board.printBoard()

                        
        drawGameState(screen, board.getBoard())
        clock.tick(MAX_FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()