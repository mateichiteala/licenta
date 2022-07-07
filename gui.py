from multiprocessing import Process, Queue
import time
# from queue import Queue
from turtle import Screen
import pygame
from board import Board
from pieces.piece import Piece
from pieces.move import Move
import ai
import monteCarlo
import pieces.move as mv
import random

WIDTH = 512
HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION

MAX_FPS = 15


class Gui():
    def __init__(self, playerOne, playerTwo, board_type=1):
        self.status_dict = {
            0: "CONTINUE",
            1: "CHECK",
            2: "CHECKMATE",
            3: "STALEMATE"
        }
        self.playerOne = True if playerOne["player"] == 0 else False
        self.playerTwo = True if playerTwo["player"] == 0 else False
        self.board_type = board_type
        self.playerOne_dict = playerOne
        self.playerTwo_dict = playerTwo
        self.IMAGES = {}
        self.loagImages()

    def loagImages(self):
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

        opening = True
        openingMoves = []

        # Read openings
        with open('openings.txt') as f:
            lines = [line.rstrip() for line in f]
        
        while running:
            humanTurn = (board.playerTurn and self.playerOne) or (not board.playerTurn and self.playerTwo)
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
                                response, move = board.guiToBoard(player_move[0], player_move[1])
                                square_selected = ()
                                player_move.clear()
                                if response:
                                    openingMoves.append(move.fromMoveToPNG())
                                else:
                                    print("Not a valid move")
                                    square_selected = ()
                                    player_move.clear()
                            else:
                                # square was selected
                                # check if it is a piece
                                piece: Piece = board.getPieceFromSquare(square_selected)
                                if piece != 0 and piece.team == board.playerTurn:
                                    validMoves = board.getValidMovesForPiece(piece)
                                    self.drawGameState(screen, board, validMoves, square_selected)
                                else:
                                    print("Not your turn")
                                    square_selected = ()
                                    player_move.clear()
            
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_z:
                        board.undoMove()
                        board.printBoard()
                        square_selected = ()
            
            if not humanTurn:
                opening = True
                if len(openingMoves) > 10:
                    opening = False

                moveMade = False
                if opening == True and len(openingMoves) > 0:
                    check = False
                    for _, line in enumerate(lines):
                        openeingMoves_str = " ".join([str(item) for item in openingMoves])
                        if line.startswith(openeingMoves_str) and len(line.split()) > len(openingMoves):
                            check = True
                            pngMove = line.split()[len(openingMoves)]
                            openingMoves.append(pngMove)
                            pos = mv.fromPNGtoMove(pngMove, board)
                            
                            if pos is None:
                                opening = False
                                break
                            
                            moveMade, move = board.guiToBoard(pos[0], pos[1])
                            
                            if moveMade is False:
                                opening = False
                                break
                    
                    if check is False:
                        opening = False

                if len(openingMoves) == 0 and self.board_type == 0:
                    # avem deschidere
                    openingLine = random.choice(lines)
                    pngMove = openingLine.split()[0]
                    openingMoves.append(pngMove)

                    pos = mv.fromPNGtoMove(pngMove, board)

                    if pos is None:
                        moveMade = False
                    else:
                        board.guiToBoard(pos[0], pos[1])
                        moveMade = True
                
                if moveMade is False:
                    ai_type = self.playerOne_dict["ai"] if board.playerTurn else self.playerTwo_dict["ai"]
                    if "simulations" in ai_type:
                        print("monte carlo")
                        aiMove = monteCarlo.MonteCarloTreeSearchNode(board, _depth_rollout=ai_type["depth"], _time=ai_type["time"]* 60, _sim=ai_type["simulations"]).best_move()
                    else:
                        print("alpha-beta")
                        validMoves = board.getValidMoves()
                        aiMove = ai.bestMoveMinMax(board, validMoves, ai_type["depth"], ai_type["time"] * 60)
                        
                    culoarea = "alb" if board.playerTurn else "negru"
                    print(f"A mutat {culoarea}")
                    
                    board.aiToBoard(aiMove)
                    time.sleep(1)

            if board.status == 3:
                board.printBoard()
                print("STALEMATE")
                while True:
                    print("STALEMATE")
            if board.status == 2:
                print("CHECKMATE")
                board.printBoard()
                while True:
                    print("CHECKMATE")
            self.drawGameState(screen, board, validMoves, square_selected)  
            if checkmate:
                self.writeOnBoard(screen, "CHECKMATE3")
            # if stalemate:
            #     writeOnBoard(screen, "STALEMATE")
            clock.tick(MAX_FPS)
            pygame.display.flip()

