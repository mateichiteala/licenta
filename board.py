from xmlrpc.client import Boolean
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


class Board:
    def __init__(self):
        self.board = 0
        self.logMoves = []
        self.IMAGES = {}
        self.playerTurn = True

        self.check = False
        self.whiteKing = 0
        self.blackKing = 0

        self.enPassantPiece = 0
        self.preveiousenPassantPiece = 0


        self.newBoard()

    def loadImages(self):
        pieces = ["wp", "bp", "wB", "bB", "wN",
                  "bN", "wR", "bR", "wQ", "bQ", "wK", "bK"]
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

    def promotionForPawn(self, piece: Pawn, pointA, pointB):
        if pointB[0] in [0, 7]:
            imgName = "wQ" if self.playerTurn == True else "bQ"
            piece = 0
            piece = Queen(self.playerTurn, 'Q',
                          self.IMAGES[imgName], pointB[0], pointB[1], False)
            self.board[pointA[0]][pointA[1]] = piece
        return piece

    def checkEnpassant(self, pawn: Pawn, pointA, pointB):
        if abs(pointB[0] - pointA[0]) == 2:
            pawn.enPassant = True
            if pawn.team:
                self.enPassantWhite = pawn
            else:
                self.enPassantBlack = pawn

        return pawn

    def enPassantMade(self, move: Move):
        # en passant was made
        direction = 1 if self.playerTurn else -1
        if 0 <= move.rowF - direction <= 7:
            if move.getPieceCaptured() == 0 and type(self.board[move.rowF - direction][move.colF]) == Pawn and self.board[move.rowF - direction][move.colF] == self.enPassantPiece:
                move.pieceCaptured =  self.board[move.rowF - direction][move.colF]
                move.enPassantPiece = self.board[move.rowF - direction][move.colF] 
                self.board[move.rowF - direction][move.colF] = 0
        return move
            
    def setEnPessant(self, piece: Piece, pointA, pointB):
        if abs(pointB[0] - pointA[0]) == 2:
            self.enPassantPiece = piece
        else:
            self.enPassantPiece = 0

    def move(self, move: Move):
        pointA = move.getInitialPos()
        pointB = move.getFinalPos()
        pieceMoved: Piece = move.getPieceMoved()

        # moves for the pieceMoved
        listMoves = pieceMoved.getMoves(self)

        # check if move in listMoves
        if move in listMoves:
            # if self.playerTurn:
            #     if self.enPassantWhite != 0:
            #         self.enPassantWhite.enPassant = False
            #     self.enPassantWhite = 0
            # else:
            #     if self.enPassantBlack != 0:
            #         self.enPassantBlack.enPassant = False
            #     self.enPassantBlack = 0

            if type(pieceMoved) == Pawn:
                pieceMoved = self.promotionForPawn(pieceMoved, pointA, pointB)
                move = self.enPassantMade(move)
                self.setEnPessant(pieceMoved, pointA, pointB)

                    

            # update log
            self.logMoves.append(move)

            # new position for the piece
            pieceMoved.setPosition(pointB[0], pointB[1])
            self.board[pointB[0]][pointB[1]] = pieceMoved
            self.board[pointA[0]][pointA[1]] = 0

            # if move.pieceMoved.type == True and move.pieceMoved.team == "K":
            #     self.whiteKing = (move.rowF, move.colF)
            # if move.pieceMoved.type == False and move.pieceMoved.team == "K":
            #     self.blackKing = (move.rowF, move.colF)

            # change turn
            self.playerTurn = not self.playerTurn

    def undoMove(self):
        if len(self.logMoves) != 0:
            move: Move = self.logMoves.pop()

            pieceMoved: Piece = move.getPieceMoved()
            pieceCaptured: Piece = move.getPieceCaptured()
            # if type(pieceCaptured) == Pawn and type(pieceMoved) == Pawn:
            #     direction = 1 if self.playerTurn else -1
            #     if move.rowF - direction == pieceCaptured.row:
            #         pieceCaptured.enPassant = True

            self.board[move.rowI][move.colI] = pieceMoved
            self.board[move.rowI][move.colI].setPosition(move.rowI, move.colI)

            if move.enPassantPiece != 0:
                self.board[move.rowF][move.colF] = 0
                self.board[pieceCaptured.row][pieceCaptured.col] = pieceCaptured
                self.enPassantPiece = pieceCaptured
            else:
                self.board[move.rowF][move.colF] = pieceCaptured
                if move.enPassantActive != 0:
                    self.enPassantPiece = pieceCaptured
                    
                if self.board[move.rowF][move.colF] != 0:
                    self.board[move.rowF][move.colF].setPosition(
                        move.rowF, move.colF)

            # if move.pieceMoved.team == True and move.pieceMoved.type == "K":
            #     self.whiteKing = (move.rowF, move.colF)
            # if move.pieceMoved.team == False and move.pieceMoved.type == "K":
            #     self.blackKing = (move.rowF, move.colF)

            self.playerTurn = not self.playerTurn  # change turn

    def getBoard(self):
        return self.board

    def isStalemate(self, playerTurn, pins):
        pieces = self.getPiecesByColor(playerTurn)
        piece: Piece
        for piece in pieces:
            moves = piece.getMoves(self)
            if len(moves) > 0:
                move: Move
                for move in moves:
                    self.move(move)
                    # verify if check after move
                    _, check, _ = self.isCheck(playerTurn)
                    if check:
                        self.undoMove()
                    else:
                        self.undoMove()
                        return False
        # the player has legal move to make
        return True

    def checksAndPins(self, kingPosition, playerTurn):
        # every direction from where the king can be attacked(without knight)
        directions = [(1, 0), (1, -1), (0, -1), (-1, -1),
                      (-1, 0), (-1, 1), (0, 1), (1, 1)]
        # pieces that can not be moved because they will create a check
        pins = []
        # pieces that check the king
        checks = []
        for direction in directions:
            allayPiece = 0
            # squares between king and the piece that checks the king
            clearSquaresDirections = []
            for i in range(1, 8):
                rowF = kingPosition[0] + direction[0] * i
                colF = kingPosition[1] + direction[1] * i
                if 0 <= rowF < 8 and 0 <= colF < 8:
                    piece: Piece = self.board[rowF][colF]
                    # check if is a piece
                    if piece != 0:
                        # check from what team is that piece
                        if piece.team != playerTurn:
                            # enemy piece
                            # can that piece attack the king ?
                            if (((piece.type == 'p' and i == 1 and (direction in [(1, 1), (-1, -1), (-1, 1), (1, -1)])) and
                                 ((playerTurn and direction[0] > 0) or (playerTurn == False and direction[0] < 0))) or
                                (piece.type == 'R' and (direction in [(0, 1), (0, -1), (-1, 0), (1, 0)])) or
                                (piece.type == 'B' and (direction in [(1, 1), (-1, -1), (-1, 1), (1, -1)])) or
                                (piece.type == 'Q') or
                                    (piece.type == 'K' and i == 1)):
                                # if allayPiece = 0 -> the king is not protected from that direction
                                if allayPiece == 0:
                                    checks.append(
                                        (piece, clearSquaresDirections))
                                # if allayPiece != 0 -> the king is not attacked but the piece that protects him is pined
                                else:
                                    pins.append(allayPiece)
                                break
                            else:
                                break
                        else:
                            # if allayPiece is already initialized with a piece -> the king is not attacked from that direction +
                            # there are no pins
                            if allayPiece != 0:
                                break
                            allayPiece = piece
                    else:
                        clearSquaresDirections.append((rowF, colF))

        # for knight
        # the knight must be captured
        knightDirections = [(1, -2), (1, 2), (-1, -2),
                            (-1, 2), (2, -1), (2, 1), (-2, -1), (-2, 1)]
        for direction in knightDirections:
            rowF = kingPosition[0] + direction[0]
            colF = kingPosition[1] + direction[1]
            if 0 <= rowF < 8 and 0 <= colF < 8:
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
        return pieces

    def escapeCheck(self, king: King, checks: list, pins: list, playerTurn: Boolean):
        validMoves = list()
        if len(checks) == 1:
            # check if capture, block or move king
            # get all pieces from a team(white: True or black: False)
            pieces = self.getPiecesByColor(playerTurn)
            piece: Piece
            for piece in pieces:
                # can I move that piece(pin)
                if piece not in pins and piece.type != "K":
                    moves = piece.getMoves(self)
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
            kingValidMoves = king.getMoves(self)
            for moveKing in kingValidMoves:
                self.move(moveKing)
                # check if king moves it will result in a check
                checksFuture, _ = self.checksAndPins(
                    king.getPosition(), playerTurn)
                if len(checksFuture) == 0:
                    validMoves.append(moveKing)
                self.undoMove()

        # only the king can move
        if len(checks) == 2:
            kingValidMoves = king.getMoves(self)
            for moveKing in kingValidMoves:
                self.move(moveKing)
                checksFuture, _ = self.checksAndPins(
                    king.getPosition(), not playerTurn)
                if len(checksFuture) == 0:
                    validMoves.append(moveKing)
                self.undoMove()

        return validMoves

    def isCheck(self, playerTurn):
        validMoves = list()
        # Get kingPosition
        if playerTurn is False:
            kingPosition = self.blackKing.getPosition()
        else:
            kingPosition = self.whiteKing.getPosition()

        check = False
        # if are any checks -> get the validMoves
        checks, pins = self.checksAndPins(kingPosition, playerTurn)
        if len(checks) > 0:
            king: King = self.board[kingPosition[0]][kingPosition[1]]
            validMoves = self.escapeCheck(king, checks, pins, self.playerTurn)
            check = True

        return validMoves, check, pins

    def guiToBoard(self, pointA, pointB, check, pins, validMoves):
        pieceMoved: Piece = self.board[pointA[0]][pointA[1]]
        pieceCaptured = self.board[pointB[0]][pointB[1]]
        move = Move(pointA, pointB, pieceMoved, pieceCaptured)

        # # en passant check
        # if type(pieceMoved) == Pawn and pieceCaptured == 0:
        #     direction = 1 if board.playerTurn else -1
        #     if 0<= player_move[1][0] - direction <= 7 and type(board.board[player_move[1][0] - direction][player_move[1][1]]) == Pawn:
        #         pieceCaptured = board.board[player_move[1][0] - direction][player_move[1][1]]
        #         move = Move(player_move[0], player_move[1], pieceMoved, pieceCaptured)

        if pieceMoved.team == self.playerTurn:
            if check:
                print("CHECK!")
                if move in validMoves:
                    self.move(move)
                else:
                    print("not valid move")
            else:
                # check stalemate
                stalemate = self.isStalemate(self.playerTurn, pins)
                if stalemate:
                    print("STALEMATE")
                if pieceMoved not in pins:
                    self.move(move)
                    # Am I in check after move
                    validMoves, check, pins = self.isCheck(not self.playerTurn)
                    if check:
                        print("not a valid move")
                        self.undoMove()
        else:
            print("Not your turn!")


if __name__ == '__main__':
    pass
