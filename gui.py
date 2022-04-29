from re import S
import pygame
from board import Board
from pieces.pawn import Pawn
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
    drawPieces(screen, board.getBoard())
    # highlightSquares(screen, board, validMoves, square_selected)



def highlightSquares(screen, board, validMoves, square_selected):
    if square_selected != ():
        row, col = square_selected
        if board.board[row][col] != 0 and board.board[row][col].team == ("w" if board.playerTurn else "b"):
            s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
            s.set_alpha(100)
            s.fill(pygame.color("blue"))
            screen.blit(s, (col*SQUARE_SIZE, row* SQUARE_SIZE))
            s.fill(pygame.Color("yellow"))
            for move in validMoves:
                if move.rowI == row and move.colI == col:
                    screen.blit(s, (SQUARE_SIZE*move.colF, SQUARE_SIZE*move.rowF))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    screen.fill(pygame.Color("white"))
    board = Board()
    
    running = True
    square_selected = ()
    player_move = []

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                # Is the player in check? Pins ? Valid moves ?
                print("SALLLL")
                validMoves, check, pins = board.isCheck(board.playerTurn)

                # If player in check and the player has no valid move to make -> checkmate
                if check and len(validMoves) == 0:
                    print("CHECKMATE")
                    running = False
                    
                # get position of the mouse
                location = pygame.mouse.get_pos()
                col = location[0] // SQUARE_SIZE
                row = location[1] // SQUARE_SIZE

                # clicked on an empty square(first) -> reset
                # clicked on the same squeare -> reset
                if (len(player_move) == 0 and board.board[row][col] == 0) or square_selected == (row, col):
                    square_selected = ()
                    player_move.clear()
                    continue
                else:
                    square_selected = (row, col)
                    player_move.append(square_selected)

                    # the player does a move
                    if len(player_move) == 2:
                        board.guiToBoard(player_move[0], player_move[1], check, pins, validMoves)
                        board.printBoard()

                        square_selected = ()
                        player_move.clear()

          
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_z:
                    board.undoMove()
                    board.printBoard()
                    square_selected = ()
          
        drawGameState(screen, board)  
        clock.tick(MAX_FPS)
        pygame.display.flip()


if __name__ == "__main__":
    main()