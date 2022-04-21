from warnings import catch_warnings
from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.piece import Piece
from pieces.queen import Queen
from pieces.rook import Rook
from builtins import range
from pieces.move import Move
import numpy as np
import pygame
from itertools import cycle

class Board:
    def __init__(self):
        self.board = 0
        self.logMoves = []
        self.IMAGES = {}
        self.playerTurn = True

        self.check = False
        self.whiteKing = 0
        self.blackKing = 0
        
        self.newBoard()


    def loadImages(self):
        pieces = ["wp", "bp", "wB", "bB", "wN", "bN", "wR", "bR", "wQ", "bQ", "wK", "bK"]
        for piece in pieces:
            self.IMAGES[piece] = pygame.image.load(f"images/{piece}.png")


    def newBoard(self):
        self.board = np.zeros((8, 8), dtype=object)  # matrix of zeros
        self.loadImages()
        self.setBoardPieces()
    

    def setBoardPieces(self):
        # set pawns
        for i in range(8):
            self.board[1][i] = Pawn(True, 'p', self.IMAGES["wp"], 1, i, False)
            self.board[6][i] = Pawn(False, 'p', self.IMAGES["bp"], 6, i, False)
        
        # set bishops
        # white
        self.board[0][2] = Bishop(True, 'B', self.IMAGES["wB"], 0, 2, False)
        self.board[0][5] = Bishop(True, 'B', self.IMAGES["wB"], 0, 5, False)
        # black
        self.board[7][2] = Bishop(False, 'B', self.IMAGES["bB"], 7, 2, False)
        self.board[7][5] = Bishop(False, 'B', self.IMAGES["bB"], 7, 5, False)

        # set knights
        # white
        self.board[0][1] = Knight(True, 'N', self.IMAGES["wN"], 0, 1, False)
        self.board[0][6] = Knight(True, 'N', self.IMAGES["wN"], 0, 6, False)
        # black
        self.board[7][1] = Knight(False, 'N', self.IMAGES["bN"], 7, 1, False)
        self.board[7][6] = Knight(False, 'N', self.IMAGES["bN"], 7, 6, False)

        # set rooks
        # white
        self.board[0][0] = Rook(True, 'R', self.IMAGES["wR"], 0, 0, False)
        self.board[0][7] = Rook(True, 'R', self.IMAGES["wR"], 0, 7, False)
        # black
        self.board[7][0] = Rook(False, 'R', self.IMAGES["bR"], 7, 0, False)
        self.board[7][7] = Rook(False, 'R', self.IMAGES["bR"], 7, 7, False)

        # set queens
        # white
        self.board[0][3] = Queen(True, 'Q', self.IMAGES["wQ"], 0, 3, False)
        # black
        self.board[7][3] = Queen(False, 'Q', self.IMAGES["bQ"], 7, 3, False)

        # set kings
        # white
        self.board[0][4] = King(True, 'K', self.IMAGES["wK"], 0, 4, False)
        self.whiteKing = self.board[0][4]
        # black
        self.board[7][4] = King(False, 'K', self.IMAGES["bK"], 7, 4, False)
        self.blackKing = self.board[7][4]

    def printBoard(self):
        boardToPrint = "#############################################################\n\n "
        boardToPrint += " | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |\n"
        i = 0
        for row in self.board:
            boardToPrint += str(i)
            for tile in row:
                if tile == 0:
                    boardToPrint += " | 0" 
                else:
                    boardToPrint += " | " + tile.type
            boardToPrint += " |\n"
            i += 1
        print(boardToPrint)
    
    def move(self, move:Move):
        pointA = move.getInitialPos()
        pointB = move.getFinalPos()
        piece: Piece = self.board[pointA[0]][pointA[1]]
        # moves for the piece
        listMoves = piece.getMoves(self.board)
        # check if pointB in listMoves

        if move in listMoves:
            self.logMoves.append(Move(move.getInitialPos(), move.getFinalPos(), move.getPieceMoved(), move.getPieceCaptured()))
            piece.setPosition(pointB[0], pointB[1])
            self.board[pointB[0]][pointB[1]] = piece
            self.board[pointA[0]][pointA[1]] = 0

            # if move.pieceMoved.type == True and move.pieceMoved.team == "K":
            #     self.whiteKing = (move.rowF, move.colF)
            # if move.pieceMoved.type == False and move.pieceMoved.team == "K":
            #     self.blackKing = (move.rowF, move.colF)

            self.playerTurn = not self.playerTurn # change turn
    
    def undoMove(self):
        if len(self.logMoves) != 0:
            move: Move = self.logMoves.pop()
            self.board[move.rowI][move.colI] = move.getPieceMoved()
            self.board[move.rowI][move.colI].setPosition(move.rowI, move.colI)
            self.board[move.rowF][move.colF] = move.getPieceCaptured()
            if self.board[move.rowF][move.colF] != 0:
                self.board[move.rowF][move.colF].setPosition(move.rowF, move.colF)

            # if move.pieceMoved.team == True and move.pieceMoved.type == "K":
            #     self.whiteKing = (move.rowF, move.colF)
            # if move.pieceMoved.team == False and move.pieceMoved.type == "K":
            #     self.blackKing = (move.rowF, move.colF)

            self.playerTurn = not self.playerTurn # change turn 
    
    def getBoard(self):
        return self.board

    def isStalemate(self, playerTurn, pins):
        pieces = self.getPiecesByColor(playerTurn)
        piece: Piece
        for piece in pieces:
            moves = piece.getMoves(self.board) 
            if len(moves) > 0:
                for move in moves:
                    self.move(move)
                    # Am I in check after move
                    validMoves, check, pins = self.isCheck(playerTurn)
                    if check:
                        self.undoMove()
                    else:
                        self.undoMove()
                        return False
        
        return True
                        
                    

    def checksAndPins(self, kingPosition, playerTurn):
        directions = [(1, 0),(1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1)]
        pins = []
        checks = []
        for direction in directions:
            allayPiece = 0
            clearSquaresDirections = []
            for i in range(1, 8):
                rowF = kingPosition[0] + direction[0] * i
                colF = kingPosition[1] + direction[1] * i
                if 0 <= rowF < 8 and 0<= colF < 8:
                    piece: Piece = self.board[rowF][colF]
                    # check if is a piece
                    if piece != 0:
                        # check from what team is that piece
                        if piece.team != playerTurn:
                            # enemy piece
                            # can that piece attack the king ?
                            if  (((piece.type == 'p' and i==1 and (direction in [(1, 1), (-1, -1), (-1, 1), (1, -1)])) and
                                ((playerTurn and direction[0] > 0) or (playerTurn == False and direction[0] < 0))) or \
                                (piece.type == 'R' and (direction in [(0, 1), (0, -1), (-1, 0), (1, 0)])) or \
                                (piece.type == 'B' and (direction in [(1, 1), (-1, -1), (-1, 1), (1, -1)])) or \
                                (piece.type == 'Q') or \
                                (piece.type == 'K' and i==1)):
                                # check
                                if allayPiece == 0:
                                    checks.append((piece, clearSquaresDirections))
                                # pin
                                else:
                                    pins.append(allayPiece)
                                break
                            else:
                                break
                           
                        else:
                            # allay piece
                            # no checks and no pins
                            if allayPiece != 0:
                                break
                            allayPiece = piece
                    else:
                        clearSquaresDirections.append((rowF, colF))

         # for knights
        knightDirections = [(1, -2), (1, 2), (-1, -2), (-1, 2), (2, -1), (2, 1), (-2, -1), (-2, 1)] 
        for direction in knightDirections:
            rowF = kingPosition[0] + direction[0]
            colF = kingPosition[1] + direction[1]
            if 0 <= rowF < 8 and 0<= colF < 8:
                piece: Piece = self.board[rowF][colF]
                if piece != 0 and piece.type == 'N' and piece.team != playerTurn:
                    checks.append((piece, list()))

        return checks, pins



    def getPiecesByColor(self, playerTurn):
        pieces = []
        for i in range(8):
            for j in range(8):
                piece: Piece = self.board[i][j]
                if piece != 0 and piece.team == playerTurn:
                    pieces.append(piece)
        print(pieces, playerTurn, len(pieces))
        return pieces


    def escapeCheck(self, king, checks, pins, playerTurn):
        validMoves = []
        if len(checks) == 1:
            # check if capture, block or move king
            pieces = self.getPiecesByColor(playerTurn)
            piece: Piece
            for piece in pieces:
                # can I move that piece(pin)
                if piece not in pins and piece.type != "K":
                    moves = piece.getMoves(self.board)
                    move: Move
                    clearSquares = checks[0][1]
                    for move in moves:
                        # can my piece capture
                        if checks[0] == move.getPieceCaptured():
                            validMoves.append(move)
                        # can my piece block
                        if move.getFinalPos() in clearSquares:
                            validMoves.append(move)
            # can my king move
            try:
                kingValidMoves = king.getMoves(self.board)
            except Exception as e:
                print(e)
            for moveKing in kingValidMoves:
                self.move(moveKing)
                checksFuture, _ = self.checksAndPins(king.getPosition(), playerTurn)
                if len(checksFuture) == 0:
                    validMoves.append(moveKing)
                self.undoMove()

        if len(checks) == 2:
            kingValidMoves = king.getMoves(self.board)
            for moveKing in kingValidMoves:
                self.move(moveKing)
                checksFuture, _ = self.checksAndPins(king.getPosition(), not playerTurn)
                if len(checksFuture) == 0:
                    validMoves.append(moveKing)
                self.undoMove()
                
        return validMoves


    def isCheck(self, playerTurn):
        if playerTurn is False:
            kingPosition = self.blackKing.getPosition()
        else:
            kingPosition = self.whiteKing.getPosition()
        
        checks = []
        pins = []
        checks, pins = self.checksAndPins(kingPosition, playerTurn)
        king: King = self.board[kingPosition[0]][kingPosition[1]]
        validMoves = []
        if len(checks) > 0:
            validMoves = self.escapeCheck(king, checks, pins, self.playerTurn)

        move: Move
        for move in validMoves:
            print(move.get())
        check = False
        print(checks)
        if len(checks) > 0:
            check = True
         
        return validMoves, check, pins


            

if __name__ == '__main__':
    # board = Board()
    direction = (1, 1)
    if direction in [(1, 1), (-1, -1), (-1, 1), (1, -1)]:
        print("sal")
    # # board.board[4][7] = Rook('W', 'R', 0, 2, 1, False)
    # board.board[1][4] = 0
    # # board.board[3][3] = Queen('W', 'Q', 0, 3, 3, False)
    # moves = board.board[0][4].getMoves(board.board)
    # board.printBoard()
    # # print(moves)
    # for move in moves:
    #     print(move.get())