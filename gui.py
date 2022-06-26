from multiprocessing import Process, Queue
from pickle import TRUE
# from queue import Queue
from re import S
import re
from tkinter.tix import Tree
from turtle import Screen
import pygame
from board import Board
from pieces.pawn import Pawn
from pieces.piece import Piece
from pieces.move import Move
import ai
import monteCarlo
import pieces.move as mv

WIDTH = 512
HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION

MAX_FPS = 15

class Gui():
    def __init__(self):
        self.IMAGES = {}
        pieces = ["wp", "bp", "wB", "bB", "wN",
                  "bN", "wR", "bR", "wQ", "bQ", "wK", "bK"]
        for piece in pieces:
            self.IMAGES[piece] = pygame.image.load(f"images/{piece}.png")
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
                    t = "w" if piece.team else "b"
                    screen.blit(self.IMAGES[t+ piece.type], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))


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
        AIThinking = False

        opening = True
        openingMoves = []

        # Read openings
        with open('openings.txt') as f:
            lines = [line.rstrip() for line in f]

        
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
                                moveMade, move = board.guiToBoard(player_move[0], player_move[1], validMoves)
                                board.printBoard()
                                square_selected = ()
                                player_move.clear()

                                if moveMade:
                                    print(move.fromMoveToPNG())
                                    openingMoves.append(move.fromMoveToPNG())
                                    # Check if the next player in stalemate, check or checkmate
                                    # Is the player in check? Pins ? Valid moves ?
                                    validMoves, check, _ = board.isCheck(board.playerTurn)
                                    stalemate = board.isStalemate(board.playerTurn)

                                    # If player in check and the player has no valid move to make -> checkmate
                                    if check and len(validMoves) == 0:
                                        print("CHECKMATE1")
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
                                    square_selected = ()
                                    player_move.clear()
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
                        # if AIThinking:
                        #     moveFinderProcess.terminate()
                        #     AIThinking = False
                        #     print("stop thinking")
                        board.printBoard()
                        square_selected = ()
            
            if not humanTurn:
                # print(openingMoves)
                if len(openingMoves) > 10:
                    opening = False

                moveMade = False
                validMoves = board.allValidMoves(board.playerTurn)
                if len(validMoves) == 0:
                    while True:
                        print("CHECKMATE2")


                if opening == True and len(openingMoves) > 0:
                    check = False
                    for index, line in enumerate(lines):
                        openeingMoves_str = " ".join([str(item) for item in openingMoves])
                        if line.startswith(openeingMoves_str) and len(line.split()) > len(openingMoves):
                            check = True
                            print(openingMoves, line)
                            pngMove = line.split()[len(openingMoves)]
                            openingMoves.append(pngMove)
                            pos = mv.fromPNGtoMove(pngMove, board)
                            # print(pngMove)

                            if pos is None:
                                opening = False
                                # print("sal")
                                break
                            # print(pos, openingMoves)
                            moveMade, move = board.guiToBoard(pos[0], pos[1], validMoves)
                            if moveMade is False:
                                opening = False
                            break
                    if check is False:
                        opening = False

                if len(openingMoves) == 0:
                    # avem deschidere
                    import random
                    openingLine = random.choice(lines)
                    # print(openingLine.split(" ")[0])
                    pngMove = openingLine.split()[0]
                    openingMoves.append(pngMove)
                    pos = mv.fromPNGtoMove(pngMove, board)
                    print(pngMove)
                    board.guiToBoard(pos[0], pos[1], validMoves)
                    moveMade = True
                
                if moveMade is False:
                    # aiMove = ai.bestMoveMinMax(board, validMoves)
                    # print(aiMove)
                    aiMove = monteCarlo.MonteCarloTreeSearchNode(board).best_move()
                    # aiMove = ai.findBestMove(board, validMoves)
                    # print(aiMove.get())
                    if aiMove is None:
                        print("AI Move is NONE`")
                        aiMove = ai.findRandomMoves(validMoves)
                    culoarea = "alb" if board.playerTurn else "negru"
                    print(f"A mutat {culoarea}")
                    
                    board.move(aiMove)
                    # if not AIThinking:
                    #     AIThinking = True
                    #     validMoves = board.allValidMoves(board.playerTurn)
                    #     if len(validMoves) == 0:
                    #         while True:
                    #             print("CHECKMATE")
                    #     AIThinking = True
                    #     print("thinking...")
                        # returnQueue = Queue()
                        # moveFinderProcess = Process(target=ai.bestMoveMinMax, args=(board, validMoves, returnQueue, ))
                        # moveFinderProcess.start()
                    
                    # if not moveFinderProcess.is_alive():
                    #     aiMove: Move = returnQueue.get()
                    #     print("done thinking")
                    #     rowI, colI = aiMove.getInitialPos()
                    #     aiMove.setPieceMoved(board.board[rowI][colI])

                    #     rowF, colF = aiMove.getFinalPos()
                    #     aiMove.setPieceCaptured(board.board[rowF][colF])

                    #     print(aiMove)
                        # if AIMove is None:
                        # aiMove = ai.bestMoveMinMax(board, validMoves)
                        # aiMove = ai.findBestMove(board, validMoves)
                        # print(aiMove.get())

                        # board.move(aiMove)
                        # AIThinking = False

            self.drawGameState(screen, board, validMoves, square_selected)  
            if checkmate:
                self.writeOnBoard(screen, "CHECKMATE3")
            # if stalemate:
            #     writeOnBoard(screen, "STALEMATE")
            clock.tick(MAX_FPS)
            pygame.display.flip()


