import time
import random

import pygame

import pieces.move as mv
from board import CODE_CHECKMATE, CODE_STALEMATE, Board
from pieces.piece import Piece
from pieces.move import Move
from alphaBeta import AlphaBeta
from monteCarlo import MonteCarloTree

WIDTH = 512
HEIGHT = 512
DIMENSION = 8
SQUARE_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15


class Gui():
    def __init__(self, playerOne, playerTwo, board_type="standard"):
        self.square_selected = ()
        self.validMoves = list()
        self.player_move = list()
        self.screen = None
        self.clock = None
        self.board = Board(board_type)
        self.openingMoves = list()
        self.openingCheck = True
        self.IMAGES = {}
        self.openingTable = list()
        self.status_dict = {
            0: "CONTINUE",
            1: "CHECK",
            2: "CHECKMATE",
            3: "STALEMATE"
        }
        self.playerOneHuman = True if playerOne["player"] == 0 else False
        self.playerTwoHuman = True if playerTwo["player"] == 0 else False
        self.board_type = board_type
        self.playerOne = playerOne
        self.playerTwo = playerTwo
        
        self.loagImages()
        self.init()
        self.loadOpenings()

    def loadOpenings(self):
        with open('openings.txt') as f:
            self.openingTable = [line.rstrip() for line in f]

    def loagImages(self):
        pieces = ["wp", "bp", "wB", "bB", "wN",
                  "bN", "wR", "bR", "wQ", "bQ", "wK", "bK"]
        for piece in pieces:
            self.IMAGES[piece] = pygame.image.load(f"images/{piece}.png")
    
    def drawBoard(self):
        colors = [pygame.Color("white"), pygame.Color("grey")]
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                color = colors[(row+col)%2]
                pygame.draw.rect(self.screen, color, pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def drawPieces(self):
        for row in range(DIMENSION):
            for col in range(DIMENSION):
                piece: Piece = self.board.board[row][col]
                if piece != 0:
                    t = "w" if piece.team else "b"
                    self.screen.blit(self.IMAGES[t+ piece.type], pygame.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def drawGameState(self):
        self.drawBoard()
        self.drawPieces()
        self.highlightSquares()

    def highlightSquares(self):
        if self.square_selected != ():
            row, col = self.square_selected
            if self.board.board[row][col] != 0 and self.board.board[row][col].team == self.board.playerTurn:
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE))
                s.set_alpha(100)
                s.fill(pygame.Color("blue"))
                self.screen.blit(s, (col*SQUARE_SIZE, row* SQUARE_SIZE))
                s.fill(pygame.Color("yellow"))
                move: Move
                for move in self.validMoves:
                    if move.rowI == row and move.colI == col:
                        self.screen.blit(s, (SQUARE_SIZE*move.colF, SQUARE_SIZE*move.rowF))

    def writeOnBoard(self, text):
        font = pygame.font.SysFont("Helvitca", 32, True, False)
        textObject = font.render(text, 0, pygame.Color("Red"))
        textLocation = pygame.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
        self.screen.blit(textObject, textLocation)

    def setAI(self):
        # ai
        print("loading...")
        if "ai" in self.playerOne:
            _time = self.playerOne["ai"]["time"] * 60
            if "simulations" in self.playerOne["ai"]:
                _sim = self.playerOne["ai"]["simulations"]
                self.playerOne = MonteCarloTree(board=self.board, _time=_time, _sim=_sim)
            else:
                _depth = self.playerOne["ai"]["depth"]
                self.playerOne = AlphaBeta(self.board, depth=_depth, time=_time)

        if "ai" in self.playerTwo:
            _time = self.playerTwo["ai"]["time"] * 60
            if "simulations" in self.playerTwo["ai"]:
                _sim = self.playerTwo["ai"]["simulations"]
                self.playerTwo = MonteCarloTree(board=self.board, _time=_time, _sim=_sim)
            else:
                _depth = self.playerTwo["ai"]["depth"]
                self.playerTwo = AlphaBeta(self.board, depth=_depth, time=_time)

    def init(self):
        pygame.init()
        pygame.display.set_caption("Chess")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen.fill(pygame.Color("white"))
        self.clock = pygame.time.Clock()
        self.drawGameState()
        self.drawGameState()  
        self.clock.tick(MAX_FPS)
        pygame.display.flip()
        self.setAI()

    def doOpening(self):
        moveMade = False
        if self.openingCheck == False or self.board_type != "standard":
            return False

        if len(self.openingMoves) > 0:
            check = False
            for _, line in enumerate(self.openingTable):
                openeingMoves_str = " ".join([str(item) for item in self.openingMoves])
                if line.startswith(openeingMoves_str) and len(line.split()) > len(self.openingMoves):
                    check = True
                    pngMove = line.split()[len(self.openingMoves)]
                    self.openingMoves.append(pngMove)
                    pos = mv.fromPNGtoMove(pngMove, self.board)
                    if pos is None:
                        self.opening = False
                        break
                    moveMade, _ = self.board.guiToBoard(pos[0], pos[1])
                    if moveMade is False:
                        self.opening = False
                        break
            if check is False:
                self.opening = False
                moveMade = False
            else:
                moveMade = True


        if len(self.openingMoves) == 0:
            # avem deschidere
            openingLine = random.choice(self.openingTable)
            pngMove = openingLine.split()[0]
            self.openingMoves.append(pngMove)
            pos = mv.fromPNGtoMove(pngMove, self.board)
            if pos is None:
                moveMade =  False
            else:
                self.board.guiToBoard(pos[0], pos[1])
                moveMade = True
                
        if len(self.openingMoves) > 10:
            self.opening = False
        
        return moveMade

    def humanTurnMove(self):
        self.square_selected = ()

        # get position of the mouse
        location = pygame.mouse.get_pos()
        col = location[0] // SQUARE_SIZE
        row = location[1] // SQUARE_SIZE

        # clicked on an empty square(first) -> reset
        # clicked on the same square -> reset
        if (len(self.player_move) == 0 and self.board.board[row][col] == 0) or self.square_selected == (row, col):
            self.square_selected = ()
            self.player_move.clear()
            return
        else:
            self.square_selected = (row, col)
            self.player_move.append(self.square_selected)

            # the player does a move
            if len(self.player_move) == 2:
                response, move = self.board.guiToBoard(self.player_move[0], self.player_move[1])
                self.square_selected = ()
                self.player_move.clear()
                if response:
                    self.openingMoves.append(move.fromMoveToPNG())
                else:
                    print("Not a valid move")
                    self.square_selected = ()
                    self.player_move.clear()
            else:
                # square was selected
                # check if it is a piece
                piece: Piece = self.board.getPieceFromSquare(self.square_selected)
                if piece != 0 and piece.team == self.board.playerTurn:
                    self.validMoves = self.board.getValidMovesForPiece(piece)
                    self.drawGameState()
                else:
                    print("Not your turn")
                    self.square_selected = ()
                    self.player_move.clear()

    def doAImove(self):
        print("AI thinking...")
        moveAI = self.playerOne.getBestMoveAI() if self.board.playerTurn else self.playerTwo.getBestMoveAI()
        culoarea = "alb" if self.board.playerTurn else "negru"
        print(f"A mutat {culoarea}")
        self.board.aiToBoard(moveAI)
   
    def start(self):
        running = True
        while running:
            humanTurn = (self.board.playerTurn and self.playerOneHuman) or (not self.board.playerTurn and self.playerTwoHuman)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    print("update database...")
                    if type(self.playerOne) == AlphaBeta:
                        self.playerOne.updateDatabase()
                    if type(self.playerTwo) == AlphaBeta:
                        self.playerTwo.updateDatabase()
                    print("exit")
                    running = False
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if humanTurn and self.board.status not in [CODE_CHECKMATE, CODE_STALEMATE]:   
                       self.humanTurnMove()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_z and (type(self.playerOne) not in [AlphaBeta, MonteCarloTree]
                    and type(self.playerTwo) not in [AlphaBeta, MonteCarloTree]):
                        self.board.undoMove()
                        self.square_selected = ()
            
            if not humanTurn and self.board.status not in [CODE_CHECKMATE, CODE_STALEMATE]:
                moveMade = self.doOpening()
                if moveMade is False:
                    self.doAImove()
                    time.sleep(1)

            if self.board.status == CODE_CHECKMATE:
                self.writeOnBoard("CHECKMATE")
                print("CHECKMATE")
                if type(self.playerOne) == AlphaBeta:
                    self.playerOne.updateDatabase()
                if type(self.playerTwo) == AlphaBeta:
                    self.playerTwo.updateDatabase()
                
                
            if self.board.status == CODE_STALEMATE:
                self.writeOnBoard("STALEMATE")
                print("STALEMATE")

            self.drawGameState()  
            self.clock.tick(MAX_FPS)
            pygame.display.flip()

        self.drawGameState()  
        self.clock.tick(MAX_FPS)
        pygame.display.flip()


