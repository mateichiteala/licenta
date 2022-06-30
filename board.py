from copy import deepcopy
from tkinter.tix import Tree
from typing import List, Union, final
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
    def __init__(self, shell=True):
        self.board = 0
        self.logMoves = list()
        self.specialMoves = list()
        self.playerTurn = True

        self.check: Boolean = False
        self.whiteKing: King = 0
        self.blackKing: King = 0

        self.enPassantPiece = 0

        self.newBoard(1)

    def newBoard(self, type: int):
        self.board = np.zeros((8, 8), dtype=object)  # matrix of zeros
        # self.loadImages()
        if type == 0:
            self.setBoardPieces()
        if type == 1:
            self.setEndgame1()
        if type == 2:
            self.setEndgame2()
    

    def setEndgame1(self):
        self.board[2][0] = Pawn(False, 'p',2, 0)
        self.board[3][1] = Pawn(False, 'p', 3, 1)
        self.board[6][7] = Pawn(False, 'p', 6, 7)

        self.board[2][6] = Rook(False, 'R',2, 6)

        self.board[7][7] = King(False, 'K', 7, 7)
        self.blackKing = self.board[7][7]



        self.board[4][1] = Pawn(True, 'p', 4, 1)

        self.board[4][3] = Rook(True, 'R', 4, 3)

        self.board[6][5] = King(True, 'K', 6, 5)
        self.whiteKing = self.board[6][5]

    def setEndgame2(self):
        self.board[2][1] = Pawn(False, 'p', 2, 1)

        self.board[1][0] = King(False, 'K', 1, 0)
        self.blackKing = self.board[1][0]


        self.board[7][5] = Rook(True, 'R', 7, 5)

        self.board[2][2] = King(True, 'K',  2, 2)
        self.whiteKing = self.board[2][2]



    def setBoardPieces(self):
       # set pawns
        for i in range(8):
            self.board[6][i] = Pawn(True, 'p', 6, i)
            self.board[1][i] = Pawn(False, 'p', 1, i)

        # set bishops
        # white
        self.board[7][2] = Bishop(True, 'B', 7, 2)
        self.board[7][5] = Bishop(True, 'B', 7, 5)
        # black
        self.board[0][2] = Bishop(False, 'B', 0, 2)
        self.board[0][5] = Bishop(False, 'B', 0, 5)

        # set knights
        # white
        self.board[7][1] = Knight(True, 'N', 7, 1)
        self.board[7][6] = Knight(True, 'N', 7, 6)
        # black
        self.board[0][1] = Knight(False, 'N', 0, 1)
        self.board[0][6] = Knight(False, 'N', 0, 6)

        # set rooks
        # white
        self.board[7][0] = Rook(True, 'R', 7, 0)
        self.board[7][7] = Rook(True, 'R', 7, 7)
        # black
        self.board[0][0] = Rook(False, 'R', 0, 0)
        self.board[0][7] = Rook(False, 'R', 0, 7)

        # set queens
        # white
        self.board[7][3] = Queen(True, 'Q', 7, 3)
        # black
        self.board[0][3] = Queen(False, 'Q', 0, 3)

        # set kings
        # white
        self.board[7][4] = King(True, 'K', 7, 4)
        self.whiteKing = self.board[7][4]
        # black
        self.board[0][4] = King(False, 'K', 0, 4)
        self.blackKing = self.board[0][4]

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
                    team = "w" if tile.team else "b"
                    boardToPrint += " | " + tile.type + team 
            boardToPrint += " |\n"
            i += 1
        print(boardToPrint)

    def promotionForPawn(self, piece: Pawn, pointA: tuple, pointB: tuple):
        # if final row position is 0, 7 than -> promotion
        if pointB[0] in [0, 7]:
            piece = Queen(self.playerTurn, 'Q', pointB[0], pointB[1])
            self.board[pointA[0]][pointA[1]] = piece
        return piece


    def enPassantMade(self, move: Move):
        # en passant was made
        direction = 1 if self.playerTurn else -1
        if 0 <= move.rowF - direction <= 7:
            # check if pieceCaptured == 0 + check the piece behind the pieceCaptured is a pawn + the piece has enPassnt activated
            opponentPawn = self.board[move.rowF - direction][move.colF]
            if move.getPieceCaptured() == opponentPawn and opponentPawn == Pawn\
                    and opponentPawn.team != self.playerTurn and opponentPawn == self.enPassantPiece:
                # set the position on the table
                self.board[move.rowF - direction][move.colF] = 0
                return True
        return False
            
    def setEnPessant(self, piece: Piece, pointA: tuple, pointB: tuple):
        # if the distance == 2 -> the piece is set to en passant
        if abs(pointB[0] - pointA[0]) == 2:
            self.enPassantPiece = piece
            return piece.getPosition()
        else:
            self.enPassantPiece = 0
            return False

    def move(self, move: Move):
        special_moves_dict = {
            "enPassantActive": 0,
            "enPassantMade": 0,
            "castleMade": 0
        }
        pointA = move.getInitialPos()
        pointB = move.getFinalPos()
        pieceMoved: Piece = move.getPieceMoved()
        pieceCaptured: Piece = move.getPieceCaptured()

        # Check pawn promotion, enpassant made and if the pawn is set to enpassant
        if type(pieceMoved) == Pawn:
            # Check pawn promotion,
            pieceMoved = self.promotionForPawn(pieceMoved, pointA, pointB)
            special_moves_dict["enPassantMade"] = self.enPassantMade(move)
            special_moves_dict["enPassantActive"] = self.setEnPessant(pieceMoved, pointA, pointB)

        # check for castling
        if type(pieceMoved) == King and type(pieceCaptured) == Rook and pieceCaptured.team == pieceMoved.team:
            direction = 1 if pieceCaptured.col > pieceMoved.col else -1
            
            # update the final position of the king and rook
            pieceMoved.setPosition(pointB[0], pointA[1] + (direction)*2)
            pieceMoved.castle = False

            pieceCaptured.setPosition(pointB[0], pointA[1] + (direction)*2 - direction)
            pieceCaptured.castle = False  

            self.board[pointB[0]][pointA[1] + (direction)*2] = pieceMoved
            self.board[pointB[0]][pointA[1] + (direction)*2 - direction] = pieceCaptured

            # update the initial position of the king and rook to zero
            self.board[pointB[0]][pointB[1]] = 0
            self.board[pointA[0]][pointA[1]] = 0

            special_moves_dict["castleMade"]  = True
        else:
            
            # If the rook was moved and has castle=True -> can not castle no more
            if type(pieceMoved) in [Rook, King]:
                pieceMoved.castle = False

            # new position for the piece
            pieceMoved.setPosition(pointB[0], pointB[1])
            # update board
            self.board[pointB[0]][pointB[1]] = pieceMoved
            self.board[pointA[0]][pointA[1]] = 0


        # update special_moves_dict
        self.specialMoves.append(special_moves_dict)
        # update log
        self.logMoves.append(move)
        # change turn
        self.playerTurn = not self.playerTurn    

    def undoMove(self):
        # There are moves to undo
        if len(self.logMoves) != 0:
            move: Move = self.logMoves.pop()
            
            pieceMoved: Piece = move.getPieceMoved()
            pieceCaptured: Piece = move.getPieceCaptured()

            initialPosition = move.getInitialPos()
            finalPosition = move.getFinalPos()
            
            # check special moves
            special_moves_dict = self.specialMoves.pop()
            
            self.playerTurn = not self.playerTurn    
            
            if special_moves_dict["castleMade"] is True:
                # we have to undo castle

                # update board

                # position of the pieces before we undo
                pieceMovedPosition = pieceMoved.getPosition()
                pieceCapturedPosition = pieceCaptured.getPosition()
                # set the King back
                pieceMoved: King
                pieceMoved.setPosition(initialPosition[0], initialPosition[1])
                pieceMoved.setCastle(True)
                self.board[initialPosition[0]][initialPosition[1]] = pieceMoved

                # set the Rook back
                pieceCaptured: Rook
                pieceCaptured.setPosition(finalPosition[0], finalPosition[1])
                pieceCaptured.setCastle(True)
                self.board[finalPosition[0]][finalPosition[1]] = pieceCaptured


                # zero the position where the King and Rook were
                self.board[pieceMovedPosition[0]][pieceMovedPosition[1]] = 0
                self.board[pieceCapturedPosition[0]][pieceCapturedPosition[1]] = 0

                return

            if special_moves_dict["enPassantActive"] != False:
                # we have to set the new pawn that is enPassant active
                # and undo move

                positionEnpassantPawn = special_moves_dict["enPassantActive"]
                # update pieces
                pieceMoved.setPosition(initialPosition[0], initialPosition[1])
                if pieceCaptured != 0:
                    pieceCaptured.setPosition(finalPosition[0], finalPosition[1])
                # update board
                self.board[initialPosition[0]][initialPosition[1]] = pieceMoved
                self.board[finalPosition[0]][finalPosition[1]] = pieceCaptured

                # update the new enPassant piece
                self.enPassantPiece = self.board[positionEnpassantPawn[0]][positionEnpassantPawn[1]]

                return



            if special_moves_dict["enPassantMade"]:
            
                self.board[pieceMoved.row][pieceMoved.col] = 0
                pieceMoved.setPosition(initialPosition[0], initialPosition[1])

                self.board[finalPosition[0]][finalPosition[1]] = 0
                self.board[pieceCaptured.row][pieceCaptured.col] = pieceCaptured
                
                # update the new enPassant piece that is the captured piece
                self.enPassantPiece = pieceCaptured

                return

            
            pieceMoved.setPosition(initialPosition[0], initialPosition[1])
            if pieceCaptured != 0:
                pieceCaptured.setPosition(finalPosition[0], finalPosition[1])
            
            self.board[initialPosition[0]][initialPosition[1]] = pieceMoved
            self.board[finalPosition[0]][finalPosition[1]] = pieceCaptured
            


            




            # # store the position of moved piece/captured piece
            # pieceMovedPosition = pieceMoved.getPosition()
            # if pieceCaptured != 0:
            #     pieceCapturedPosition = pieceCaptured.getPosition()

            # # update the position of the moved piece
            # self.board[move.rowI][move.colI] = pieceMoved
            # pieceMoved.setPosition(move.rowI, move.colI)
            # self.board[move.rowI][move.colI].setPosition(move.rowI, move.colI)
            

            # self.enPassantlist.pop()        
            # # Piece made en passant
            # if move.enPassantPiece != 0: 
            #     self.board[move.rowF][move.colF] = 0
            #     self.board[pieceCaptured.row][pieceCaptured.col] = pieceCaptured
            #     # update the new enPassant piece
            #     self.enPassantPiece = pieceCaptured
            # else:
            #     # check if there is a new en passant piece
            #     if len(self.enPassantlist) > 0:
            #         # get the current state of the board
            #         enPassant = self.enPassantlist[len(self.enPassantlist) - 1]
            #         # set the new en passant
            #         if enPassant == True:
            #             presentMove: Move = self.logMoves[len(self.logMoves) - 1]
            #             self.enPassantPiece = presentMove.getPieceMoved()
            #         else:
            #             self.enPassantPiece == 0
                
            #     # set the pieceCaptured on the board and position(if != 0)
            #     self.board[move.rowF][move.colF] = pieceCaptured
            #     if self.board[move.rowF][move.colF] != 0:
            #         self.board[move.rowF][move.colF].setPosition(
            #             move.rowF, move.colF)
                
            #     if move.castleIndex == True:
            #         if pieceCaptured != 0:
            #             pass
            #             # print(pieceCaptured.type)
            #         pieceMoved.castle = True
                    
            #     # check if the undo move reset the castle status
            #     # if len(self.indexFirstMoveKingAndRook) > 0 and len(self.logMoves) == self.indexFirstMoveKingAndRook[len(self.indexFirstMoveKingAndRook)-1]:
                    
            #     #     pieceMoved.castle = True
            #     #     self.indexFirstMoveKingAndRook.pop()
                

            #     # Castle was made
            #     if type(pieceMoved) == King and type(pieceCaptured) == Rook and pieceCaptured.team == pieceMoved.team:

            #         # set the king back
            #         # self.board[move.rowI][move.colI] = pieceMoved
            #         self.board[move.rowI][move.colI].castle = True
            #         # self.board[move.rowI][move.colI].setPosition(move.rowI, move.colI)

            #         # set the rook back
            #         self.board[move.rowF][move.colF] = pieceCaptured
            #         self.board[move.rowF][move.colF].castle = True
            #         self.board[move.rowF][move.colF].setPosition(move.rowF, move.colF)

            #         # zero the position
            #         self.board[pieceMovedPosition[0]][pieceMovedPosition[1]] = 0
            #         self.board[pieceCapturedPosition[0]][pieceCapturedPosition[1]] = 0

            # self.playerTurn = not self.playerTurn  # change turn

    def getBoard(self):
        return self.board

    def isStalemate(self, playerTurn: bool):
        # Get all the pieces from that team
        pieces = self.getPiecesByColor(playerTurn)

        piece: Piece
        for piece in pieces:
            # Get all moves
            moves = piece.getMoves(self)
            if len(moves) > 0:
                move: Move
                for move in moves:
                    # verify if check after move
                    # If there are no checks -> no stalemate
                    self.move(move)
                    _, check, _ = self.isCheck(playerTurn)
                    self.undoMove()

                    if check == False:
                        return False

        # the player has no legal move to make
        return True

    def checksAndPins(self, playerTurn: Boolean):
        king: King = self.whiteKing if playerTurn else self.blackKing
        kingPosition = king.getPosition()
        # Every direction from where the king can be attacked(without the knight)
        directions = [(1, 0), (1, -1), (0, -1), (-1, -1),
                      (-1, 0), (-1, 1), (0, 1), (1, 1)]

        # Pieces that can not be moved because they will create a check
        pins = []
        
        # Pieces that check the king
        # checks contains the piece that attacks the king and clearSquaresDirections
        checks = []

        for direction in directions:
            # Used to check if there is an allay piece between the king and the piece that attacks
            allayPiece = 0
            
            # Squares between king and the piece that checks the king
            clearSquaresDirections = []
            
            for i in range(1, 8):
                rowF = kingPosition[0] + direction[0] * i
                colF = kingPosition[1] + direction[1] * i

                if 0 <= rowF < 8 and 0 <= colF < 8:
                    piece: Piece = self.board[rowF][colF]
                    
                    # Check if it is a piece
                    if piece != 0:
                        # Check from what team is that piece
                        if piece.team != playerTurn:
                            # enemy piece, can that piece attack the king ?
                            if (((piece.type == 'p' and i == 1 and (direction in [(1, 1), (-1, -1), (-1, 1), (1, -1)])) and
                                 ((playerTurn and direction[0] < 0) or (playerTurn == False and direction[0] > 0))) or
                                (piece.type == 'R' and (direction in [(0, 1), (0, -1), (-1, 0), (1, 0)])) or
                                (piece.type == 'B' and (direction in [(1, 1), (-1, -1), (-1, 1), (1, -1)])) or
                                (piece.type == 'Q') or
                                    (piece.type == 'K' and i == 1)):
                                # if allayPiece == 0 -> the king is not protected from that direction
                                if allayPiece == 0:
                                    checks.append(
                                        (piece, clearSquaresDirections))
                                # if allayPiece != 0 -> the king is not attacked but the piece that protects is pined
                                else:
                                    pins.append(allayPiece)
                            # the iteration stops on that direction
                            break
                        else:
                            # if allayPiece is already initialized with a piece -> the king is not attacked from that direction +
                            # there are no pins(on that direction)
                            # the iteration stops on that direction
                            if allayPiece != 0:
                                break
                            # possible a pin
                            allayPiece = piece
                    else:
                        # add squares between king and the attack piece(if that exists)
                        clearSquaresDirections.append((rowF, colF))

        # for knight
        # the knight must be captured(can not be blocked)
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

    def getPiecesByColor(self, playerTurn: Boolean):
        pieces = list()
        for i in range(8):
            for j in range(8):
                piece: Piece = self.board[i][j]
                if piece != 0 and piece.team == playerTurn:
                    pieces.append(piece)
        return pieces

    def escapeCheck(self, king: King, checks: list, pins: list, playerTurn: Boolean):
        validMoves = list()
        # If there is only one check -> capture, block or move king
        if len(checks) == 1:
            # get all pieces from a team(white: True or black: False)
            pieces = self.getPiecesByColor(playerTurn)
            
            piece: Piece
            for piece in pieces:
                # can I move that piece(check if it is pin)
                if piece not in pins and piece.type != "K":
                    # Get the clear squares in order to block the attack
                    clearSquares = checks[0][1]
                    pieceThatChecks: Piece = checks[0][0]
                    moves = piece.getMoves(self)
                    
                    move: Move
                    for move in moves:
                        # can my piece capture
                        if pieceThatChecks == move.getPieceCaptured():
                            validMoves.append(move)
                        
                        # can my piece block
                        if move.getFinalPos() in clearSquares:
                            validMoves.append(move)
            
            # Can the king move
            kingValidMoves = king.getMoves(self)
            for moveKing in kingValidMoves:
                self.move(moveKing)
                # check if king moves it will result in a check
                checksFuture, _ = self.checksAndPins(playerTurn)
                if len(checksFuture) == 0:
                    # that king has a valid move to make
                    validMoves.append(moveKing)
                self.undoMove()

        # only the king can move
        if len(checks) == 2:
            kingValidMoves = king.getMoves(self)
            for moveKing in kingValidMoves:
                self.move(moveKing)
                # check if king moves it will result in a check
                checksFuture, _ = self.checksAndPins(playerTurn)
                if len(checksFuture) == 0:
                    # that king has a valid move to make
                    validMoves.append(moveKing)
                self.undoMove()

        return validMoves

    def isCheck(self, playerTurn: Boolean):
        # ValidMoves to escape check
        validMoves = list()

        # Get king
        king: King = self.whiteKing if playerTurn else self.blackKing

        # If there are any checks -> get the validMoves
        check = False
        checks, pins = self.checksAndPins(playerTurn)
        if len(checks) > 0:
            validMoves = self.escapeCheck(king, checks, pins, self.playerTurn)
            check = True
        else:
            validMoves.append(1)

        return validMoves, check, pins

    def getAllPiecesByTypeAndTurn(self, type:str, playerTurn: bool):
        pieces = list()
        for i in range(8):
            for j in range(8):
                piece: Piece = self.board[i][j]
                if piece != 0 and piece.type == type and piece.team == playerTurn:
                    pieces.append(piece)
        return pieces

    def validMovesPiece(self, point: Union[tuple, Piece]):
        validMoves = list()
        if type(point) == tuple:
            row = point[0]
            col = point[1]
            pieceSelected: Piece = self.board[row][col]
        else:
            pieceSelected = point

        if pieceSelected != 0:
            moves = pieceSelected.getMoves(self)
            move: Move
            for move in moves:
                self.move(move)
                _, check, _ = self.isCheck(not self.playerTurn)
                if check == False:
                    validMoves.append(move)
                self.undoMove()

        return validMoves

    def allValidMoves(self, playerTurn: bool):
        validMoves = list()
        pieces = self.getPiecesByColor(playerTurn)
        for piece in pieces:
            validMoves.extend(self.validMovesPiece(piece))
        
        return validMoves

    def guiToBoard(self, pointA, pointB, validMoves):
        pieceMoved: Piece = self.board[pointA[0]][pointA[1]]
        pieceCaptured: Piece = self.board[pointB[0]][pointB[1]]
        move = Move(pointA, pointB, pieceMoved, pieceCaptured)

        if move in validMoves:
            self.move(move)
            return True, move

        return False, move


    def statusBoard(self, playerTurn=None):
        # Check if the player in stalemate, check or checkmate
        # Is the player in check? Pins ? Valid moves ?
        if playerTurn is None:
            playerTurn = self.playerTurn
        validMoves, check, _ = self.isCheck(playerTurn)

        # If player in check and the player has no valid move to make -> checkmate

        if len(validMoves) == 0 and check == False:
            return 3

        if check and len(validMoves) == 0:
            return 2



        if check and len(validMoves) > 0:
            return 1

        return 0
        
    def checkMate(self):
        validMoves, check, _ = self.isCheck(self.playerTurn)
        return True if check and len(validMoves) == 0 else False
            
       

if __name__ == '__main__':
    pass
