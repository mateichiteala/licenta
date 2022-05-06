from pickle import TRUE
from re import S
from tkinter.tix import Tree
from turtle import Screen
import pygame
from board import Board
from pieces.pawn import Pawn
from pieces.piece import Piece
from pieces.move import Move
import ai

WIDTH = 512
HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION

MAX_FPS = 15

class Gui():
    def drawBoard(self, screen):
        colors = [pygame.Color("white"), pygame.Color("grey")]
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                color = colors[(row+col)%2]
                pygame.draw.rect(screen, color, pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    def drawPieces(self, screen, board):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                piece: Piece = board[row][col]
                if piece != 0:
                    screen.blit(piece.getImage(), pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


    def drawGameState(self, screen, board, validMoves, square_selected):
        self.drawBoard(screen)
        self.drawPieces(screen, board.getBoard())
        self.highlightSquares(screen, board, validMoves, square_selected)



    def highlightSquares(self, screen, board, validMoves, square_selected):
        if square_selected != ():
            row, col = square_selected
            if board.board[row][col] != 0 and board.board[row][col].team == board.playerTurn:
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                s.set_alpha(100)
                s.fill(pygame.Color("blue"))
                screen.blit(s, (col*SQUARE_SIZE, row* SQUARE_SIZE))
                s.fill(pygame.Color("yellow"))
                move: Move
                for move in validMoves:
                    if move.rowI == row and move.colI == col:
                        screen.blit(s, (SQUARE_SIZE*move.colF, SQUARE_SIZE*move.rowF))


    def writeOnBoard(self, screen, text):
        font = pygame.font.SysFont("Helvitca", 32, True, False)
        textObject = font.render(text, 0, pygame.Color("Red"))
        textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
        screen.blit(textObject, textLocation)


    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        clock = pygame.time.Clock()
        screen.fill(pygame.Color("white"))
        board = Board()
        
        running = True
        validMoves = []
        square_selected = ()
        player_move = []
        checkmate = False
        stalemate = False
        # true - human, false - computer
        playerOne = True
        playerTwo = False

        while running:
            humanTurn = (board.playerTurn and playerOne) or (not board.playerTurn and playerTwo)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if humanTurn:   
                        # get position of the mouse
                        location = pygame.mouse.get_pos()
                        col = location[0] // SQUARE_SIZE
                        row = location[1] // SQUARE_SIZE

                        # clicked on an empty square(first) -> reset
                        # clicked on the same square -> reset
                        if (len(player_move) == 0 and board.board[row][col] == 0) or square_selected == (row, col):
                            square_selected = ()
                            player_move.clear()
                            continue
                        else:
                            square_selected = (row, col)
                            player_move.append(square_selected)

                            # the player does a move
                            if len(player_move) == 2:
                                moveMade = board.guiToBoard(player_move[0], player_move[1], validMoves)
                                board.printBoard()

                                square_selected = ()
                                player_move.clear()

                                if moveMade:
                                    # Check if the next player in stalemate, check or checkmate
                                    # Is the player in check? Pins ? Valid moves ?
                                    validMoves, check, _ = board.isCheck(board.playerTurn)
                                    stalemate = board.isStalemate(board.playerTurn)

                                    # If player in check and the player has no valid move to make -> checkmate
                                    if check and len(validMoves) == 0:
                                        print("CHECKMATE")
                                        checkmate = True
                                        continue
                                    if stalemate:
                                        print("STALEMATE")
                                        stalemate = True
                                        continue
                                        # running = False
                                    if check and len(validMoves) > 0:
                                        print("CHECK")
                                        # running = False

                                else:
                                    print("not a valid move")
                            else:
                                if board.board[square_selected[0]][square_selected[1]] != 0 and board.board[square_selected[0]][square_selected[1]].team == board.playerTurn:
                                    validMoves = board.validMovesPiece(square_selected)
                                    self.drawGameState(screen, board, validMoves, square_selected)
                                else:
                                    print("not your turn")
                                    square_selected = ()
                                    player_move.clear()
            
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_z:
                        board.undoMove()
                        board.printBoard()
                        square_selected = ()
            
            if not humanTurn:
                validMoves = board.allValidMoves(board.playerTurn)
                if len(validMoves) == 0:
                    while True:
                        print("CHECKMATE")
                aiMove = ai.bestMoveMinMax(board, validMoves)
                # aiMove = ai.findBestMove(board, validMoves)
                # print(aiMove.get())
                if aiMove is None:
                    print("sal")
                    aiMove = ai.findRandomMoves(validMoves)
                board.move(aiMove)
            
            self.drawGameState(screen, board, validMoves, square_selected)  
            if checkmate:
                self.writeOnBoard(screen, "CHECKMATE")
            # if stalemate:
            #     writeOnBoard(screen, "STALEMATE")
            clock.tick(MAX_FPS)
            pygame.display.flip()


