
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

CODE_STALEMATE = 3
CODE_CHECKMATE = 2
CODE_CHECK = 1
CODE_NORMAL = 0

STALEMATE = 0
CHECKMATE = 50000
CHECK = 900

class Board:
    def __init__(self):
        self.board = 0
        self.logMoves = list()
        self.states = list()

        self.playerTurn = True
        

        # self.piecesThatChecks = list()
        self.pins = list()
        self.attackPins = list()

        self.whiteKing: King = 0
        self.blackKing: King = 0

        self.enPassantPiece = 0
        self.valid_moves = list()
        self.status = 0

        self.newBoard("endgame3")
        self.setValidMoves()
        self.setStatus()



    def newBoard(self, type: int):
        self.board = np.zeros((8, 8), dtype=object)  # matrix of zeros
        board_dict = {
            "standard": self.setBoardPieces,
            "endGame1": self.endgame1,
            "endGame2": self.endgame2,
            "twoRookMate": self.twoRookMate,
            "endgame3": self.endgame3
        }
        board_dict[type]()
    

    def endgame3(self):
        """GM Judit Polgar (2686) - GM Veselin Topalov (2786)
        Ajedrez UNAM KO Mexico City MEX, 2010.11.21
        White to win"""
        self.board[0][2] = King(False, 0, 2)
        self.blackKing = self.board[0][2]
        self.blackKing.castle = False
        self.blackKing.firstMoveIndex = -1
        
        self.board[0][4] = Rook(False, 0, 4)

        self.board[1][0] = Pawn(False, 1, 0)
        self.board[1][2] = Pawn(False, 1, 2)
        self.board[1][3] = Rook(False, 1, 3)
        self.board[1][5] = Pawn(False, 1, 5)
        self.board[1][6] = Bishop(False, 1, 6)

        self.board[2][1] = Pawn(False, 2, 1, initilialPosSet=False)
        self.board[2][3] = Pawn(True, 2, 3,  initilialPosSet=False)
        self.board[2][6] = Knight(True, 2, 6)
        self.board[2][7] = Pawn(False, 2, 7,  initilialPosSet=False)

        self.board[3][2] = Pawn(False, 3, 2, initilialPosSet=False)
        self.board[3][4] = Pawn(True, 3, 4, initilialPosSet=False)
        self.board[3][6] = Pawn(False, 3, 6, initilialPosSet=False)
        
        self.board[4][6] = Pawn(True, 4, 6, initilialPosSet=False)

        self.board[5][1] = Pawn(True, 5, 1, initilialPosSet=False)
        self.board[5][5] = Knight(True, 5, 5)
        self.board[5][7] = Pawn(True, 5, 7, initilialPosSet=False)

        self.board[6][0] = Pawn(True, 6, 0)
        self.board[6][1] = Bishop(True, 6, 1)
        self.board[6][3] = Rook(True, 6, 3)
        self.board[6][5] = Pawn(True, 6, 5)
        self.board[6][7] = King(True, 6, 7)
        self.whiteKing = self.board[6][7]
        self.whiteKing.castle = False
        self.whiteKing.firstMoveIndex = -1

        self.board[7][3] = Rook(True, 7, 3)


    def twoRookMate(self):
        self.board[1][4] = King(False, 1, 4)
        self.blackKing = self.board[1][4]

        self.board[7][7] = Rook(True, 7, 7)
        self.board[2][0] = Rook(True, 2, 0)
        self.board[7][3] = King(True, 7, 3)
        self.whiteKing = self.board[7][3]
        self.whiteKing.castle = False

    def endgame1(self):
        # self.board[2][0] = Pawn(False, 'p',2, 0)
        self.board[3][1] = Pawn(False, 3, 1)
        self.board[6][7] = Pawn(False, 6, 7)

        self.board[2][6] = Rook(False, 2, 6)

        self.board[7][7] = King(False, 7, 7)
        self.blackKing = self.board[7][7]



        self.board[4][1] = Pawn(True, 4, 1)

        self.board[4][3] = Rook(True, 4, 3)

        self.board[6][5] = King(True, 6, 5)
        self.whiteKing = self.board[6][5]

    def endgame2(self):
        self.board[2][1] = Pawn(False, 2, 1)

        self.board[1][0] = King(False, 1, 0)
        self.blackKing = self.board[1][0]


        self.board[7][5] = Rook(True, 7, 5)

        self.board[2][2] = King(True, 2, 2)
        self.whiteKing = self.board[2][2]

    def endgame1(self):
            # self.board[2][0] = Pawn(False, 'p',2, 0)
            self.board[3][1] = Pawn(False, 3, 1)
            self.board[6][7] = Pawn(False, 6, 7)

            self.board[2][6] = Rook(False, 2, 6)

            self.board[7][7] = King(False, 7, 7)
            self.blackKing = self.board[7][7]



            self.board[4][1] = Pawn(True, 4, 1)

            self.board[4][3] = Rook(True, 4, 3)

            self.board[6][5] = King(True, 6, 5)
            self.whiteKing = self.board[6][5]



    def setBoardPieces(self):
       # set pawns
        for i in range(8):
            self.board[6][i] = Pawn(True,  6, i)
            self.board[1][i] = Pawn(False,  1, i)

        # set bishops
        # white
        self.board[7][2] = Bishop(True, 7, 2)
        self.board[7][5] = Bishop(True, 7, 5)
        # black
        self.board[0][2] = Bishop(False, 0, 2)
        self.board[0][5] = Bishop(False, 0, 5)

        # set knights
        # white
        self.board[7][1] = Knight(True, 7, 1)
        self.board[7][6] = Knight(True, 7, 6)
        # black
        self.board[0][1] = Knight(False, 0, 1)
        self.board[0][6] = Knight(False, 0, 6)

        # set rooks
        # white
        self.board[7][0] = Rook(True, 7, 0)
        self.board[7][7] = Rook(True, 7, 7)
        # black
        self.board[0][0] = Rook(False, 0, 0)
        self.board[0][7] = Rook(False, 0, 7)

        # set queens
        # white
        self.board[7][3] = Queen(True, 7, 3)
        # black
        self.board[0][3] = Queen(False, 0, 3)

        # set kings
        # white
        self.board[7][4] = King(True, 7, 4)
        self.whiteKing = self.board[7][4]
        # black
        self.board[0][4] = King(False, 0, 4)
        self.blackKing = self.board[0][4]

    def printBoard(self):
        boardToPrint = "#############################################################\n\n "
        boardToPrint += "|  0  |  1  |  2  |  3  |  4  |  5  |  6  |  7  |\n"
        i = 0
        for row in self.board:
            boardToPrint += str(i)
            for tile in row:
                if tile == 0:
                    boardToPrint += " | 0"
                else:
                    team = "w" if tile.team else "b"
                    boardToPrint += "  |  " + tile.type + team 
            boardToPrint += " |\n"
            i += 1
        print(boardToPrint)

    def promotionForPawn(self, piece: Pawn, pointA: tuple, pointB: tuple):
        # if final row position is 0, 7 than -> promotion
        if pointB[0] in [0, 7]:
            piece = Queen(self.playerTurn, pointB[0], pointB[1])
            self.board[pointB[0]][pointB[1]] = piece
        return piece


    def enPassantMade(self, move: Move):
        # en passant was made
        direction = 1 if self.playerTurn else -1
        if 0 <= move.rowF + direction <= 7:
            # check if pieceCaptured == 0 + check the piece behind the pieceCaptured is a pawn + the piece has enPassnt activated
            opponentPawn = self.board[move.rowF+direction][move.colF]

            if move.getPieceCaptured() == opponentPawn and type(opponentPawn) == Pawn\
                    and opponentPawn.team != self.playerTurn and opponentPawn == self.enPassantPiece:
                # set the position on the table
                self.board[move.rowF + direction][move.colF] = 0
                return True
        return False
            
    def setEnPessant(self, piece: Piece, pointA: tuple, pointB: tuple):
        # if the distance == 2 -> the piece is set to en passant
        if type(piece) == Pawn and abs(pointB[0] - pointA[0]) == 2:
            self.enPassantPiece = piece
        else:
            self.enPassantPiece = 0
    
    def getEnpassantPiece(self):
        if self.enPassantPiece != 0:
            return self.board[self.enPassantPiece.row][self.enPassantPiece.col]
        else:
            return 0

    def move(self, move: Move):
        state_dict = {
            # after move
            "enPassantMade": 0,
            "castleMade": 0,
            # before move
            "enPassantActive": self.getEnpassantPiece(), 
            "status": self.status, 
            "valid_moves": self.getValidMoves(),
            "pins": self.pins,
            "attackPins": self.attackPins
        }
        if self.blackKing.castle is True:
            print("Yo")
        pointA = move.getInitialPos()
        pointB = move.getFinalPos()
        pieceMoved: Piece = move.getPieceMoved()
        pieceCaptured: Piece = move.getPieceCaptured()        

        if pieceMoved == 0:
            print("aici")
            self.printBoard()
        # Check pawn promotion, enpassant made and if the pawn is set to enpassant
        if type(pieceMoved) == Pawn:
            # Check pawn promotion,
            pieceMoved = self.promotionForPawn(pieceMoved, pointA, pointB)
            state_dict["enPassantMade"] = self.enPassantMade(move)
        
        self.setEnPessant(pieceMoved, pointA, pointB)
        # check for castling
        if type(pieceMoved) == King and type(pieceCaptured) == Rook and pieceCaptured.team == pieceMoved.team and\
            (pieceMoved.castle == True and pieceCaptured.castle == True):
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

            state_dict["castleMade"]  = True

        else:
            
            # If the rook was moved and has castle=True -> can not castle no more
            if type(pieceMoved) in [Rook, King]:
                pieceMoved.castle = False
                if pieceMoved.firstMoveIndex not in [None, -1]:
                    pieceMoved.firstMoveIndex = len(self.logMoves)

            # new position for the piece
            pieceMoved.setPosition(pointB[0], pointB[1])
            # update board
            self.board[pointB[0]][pointB[1]] = pieceMoved
            self.board[pointA[0]][pointA[1]] = 0
        
        self.states.append(state_dict)
        
        if self.blackKing.castle is True:
            print("Yo")
        # update log
        self.logMoves.append(move)
        # update board
        self.playerTurn = not self.playerTurn
        
        return True
        

    def undoMove(self):
        # There are moves to undo
        if len(self.logMoves) != 0:
            move: Move = self.logMoves.pop()
            
            pieceMoved: Piece = move.getPieceMoved()
            pieceCaptured: Piece = move.getPieceCaptured()

            initialPosition = move.getInitialPos()
            finalPosition = move.getFinalPos()
            
            # get current state
            state_dict = self.states.pop()
            
            self.playerTurn = not self.playerTurn
            
            # update state with the old info
            self.status = state_dict["status"]
            self.valid_moves = state_dict["valid_moves"]
            self.pins = state_dict['pins']
            self.attackPins = state_dict["attackPins"]

            
            if state_dict["castleMade"] is True:
                # we have to undo castle

                # update board

                # position of the pieces before we undo
                pieceMovedPosition = pieceMoved.getPosition()
                pieceCapturedPosition = pieceCaptured.getPosition()
                
                # set the King back
                pieceMoved: King
                pieceMoved.firstMoveIndex = None
                pieceMoved.setPosition(initialPosition[0], initialPosition[1])
                pieceMoved.setCastle(True)
                self.board[initialPosition[0]][initialPosition[1]] = pieceMoved

                # set the Rook back
                pieceCaptured: Rook
                pieceCaptured.firstMoveIndex = None
                pieceCaptured.setPosition(finalPosition[0], finalPosition[1])
                pieceCaptured.setCastle(True)
                self.board[finalPosition[0]][finalPosition[1]] = pieceCaptured


                # zero the position where the King and Rook were
                self.board[pieceMovedPosition[0]][pieceMovedPosition[1]] = 0
                self.board[pieceCapturedPosition[0]][pieceCapturedPosition[1]] = 0
                
                return
            

            # if state_dict["enPassantActive"] is True:
            #     self.enPassantPiece = state_dict[]
                # # we have to set the new pawn that is enPassant active
                # # and undo move

                # positionEnpassantPawn = state_dict["enPassantActive"]
                # # update pieces
                # pieceMoved.setPosition(initialPosition[0], initialPosition[1])
                # # if pieceCaptured != 0:
                # #     pieceCaptured.setPosition(finalPosition[0], finalPosition[1])
                # # update board
                # self.board[initialPosition[0]][initialPosition[1]] = pieceMoved
                # self.board[finalPosition[0]][finalPosition[1]] = pieceCaptured

                # # update the new enPassant piece
                # self.enPassantPiece = self.board[positionEnpassantPawn[0]][positionEnpassantPawn[1]]
                # if pieceMoved == 0:
                #     print("sal4")
                # return

            if state_dict["enPassantMade"] is True:
            
                self.board[pieceMoved.row][pieceMoved.col] = 0
                
                pieceMoved.setPosition(initialPosition[0], initialPosition[1])
                self.board[initialPosition[0]][initialPosition[1]] = pieceMoved

                self.board[finalPosition[0]][finalPosition[1]] = 0
                self.board[pieceCaptured.row][pieceCaptured.col] = pieceCaptured
                
                # update the new enPassant piece that is the captured piece
                self.enPassantPiece = pieceCaptured
                return

            self.enPassantPiece = state_dict["enPassantActive"]
            
            pieceMoved.setPosition(initialPosition[0], initialPosition[1])

            if type(pieceMoved) in [King, Rook] and pieceMoved.firstMoveIndex == len(self.logMoves):
                pieceMoved.castle = True
                pieceMoved.firstMoveIndex = None
                
            if pieceCaptured != 0:
                pieceCaptured.setPosition(finalPosition[0], finalPosition[1])
            
            self.board[initialPosition[0]][initialPosition[1]] = pieceMoved
            self.board[finalPosition[0]][finalPosition[1]] = pieceCaptured

                        
    def getBoard(self):
        return self.board

    def getChecksAndPins(self, player):
        king: King = self.whiteKing if player else self.blackKing
        kingPosition = king.getPosition()
        # Every direction from where the king can be attacked(without the knight)
        directions = [(1, 0), (1, -1), (0, -1), (-1, -1),
                      (-1, 0), (-1, 1), (0, 1), (1, 1)]

        # Pieces that can not be moved because they will create a check
        pins = []
        
        # Enemy pieces that attack the pin
        attackPins = []

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
                        if piece.team != player:
                            # enemy piece, can that piece attack the king ?
                            if (((piece.type == 'p' and i == 1 and 
                                (direction in [(1, 1), (-1, -1), (-1, 1), (1, -1)])) and
                                ((player and direction[0] < 0) or (player == False and direction[0] > 0))) or
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
                                    attackPins.append((piece, direction))
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
                if piece != 0 and piece.type == 'N' and piece.team != player:
                    checks.append((piece, list()))

        return checks, pins, attackPins

    def getPiecesByColor(self, player: Boolean):
        pieces = list()
        for i in range(8):
            for j in range(8):
                piece: Piece = self.board[i][j]
                if piece != 0 and piece.team == player:
                    pieces.append(piece)
        return pieces

    def getEscapeCheckValidMoves(self):
        player = self.playerTurn
        validMoves = list()
        king: King = self.whiteKing if player else self.blackKing
        # If there is only one check -> capture, block or move king
        if len(self.checks) == 1:
            # get all pieces from a team(white: True or black: False)
            pieces = self.getPiecesByColor(player)
            
            piece: Piece
            for piece in pieces:
                # can I move that piece(check if it is pin)
                if piece not in self.pins and piece.type != "K":
                    # Get the clear squares in order to block the attack
                    clearSquares = self.checks[0][1]
                    pieceThatChecks: Piece = self.checks[0][0]
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
            for move in kingValidMoves:
                if self.checkIfMoveIsValid(player, move):
                    validMoves.append(move)

        # only the king can move
        if len(self.checks) == 2:
            kingValidMoves = king.getMoves(self)
            for move in kingValidMoves:
                if self.checkIfMoveIsValid(player, move):
                    validMoves.append(move)

        return validMoves

    def getAllPiecesByTypeAndTurn(self, type:str, player: bool):
        pieces = list()
        for i in range(8):
            for j in range(8):
                piece: Piece = self.board[i][j]
                if piece != 0 and piece.type == type and piece.team == player:
                    pieces.append(piece)
        return pieces

    def checkIfMoveIsValid(self, player, move):
        self.move(move)
        checks, _, _ = self.getChecksAndPins(player)
        self.undoMove()
        return False if len(checks) > 0 else True


    def getValidMovesForPiece(self, piece: Piece):
        piece_moves = piece.getMoves(self)
        valid_moves_piece = list()
        
        move: Move
        for move in piece_moves:
            if move in self.valid_moves:
                valid_moves_piece.append(move)
        return valid_moves_piece 

    def validMovesPieceWithChecking(self, point: Union[tuple, Piece]):
        """Valid moves for a piece or square"""
        validMoves = list()
        if type(point) == tuple:
            row = point[0]
            col = point[1]
            pieceSelected: Piece = self.board[row][col]
        else:
            pieceSelected = point

        if pieceSelected != 0:
            # all moves without verifing for checks, pins, etc...
            moves = pieceSelected.getMoves(self)
            move: Move
            for move in moves:
                pieceMoved: Piece = move.getPieceMoved()
                # King can not be pinned. But if he moves can be checked
                if type(pieceMoved) == King:
                    if self.checkIfMoveIsValid(self.playerTurn, move) is False:
                        continue
                
                #TODO verificare pentru pin mutat
                attackPins = list()
                for attackPin in self.attackPins:
                    attackPins.append(attackPin[0]) 
                if pieceMoved not in self.pins or move.getPieceCaptured() in attackPins:
                    validMoves.append(move)

        return validMoves

    def allValidMoves(self, playerTurn: bool, pins, attackPins):
        """Valid moves for a player"""
        validMoves = list()
        pieces = self.getPiecesByColor(playerTurn)
        for piece in pieces:
            validMoves.extend(self.validMovesPieceWithChecking(piece, pins, attackPins))
        
        return validMoves
    
    def getValidMoves(self):
        return self.valid_moves

    def setValidMoves(self):
        validMoves = list()
        pieces = self.getPiecesByColor(self.playerTurn)
        self.checks, self.pins, self.attackPins = self.getChecksAndPins(self.playerTurn)
        
        if len(self.checks) > 0:
            validMoves = self.getEscapeCheckValidMoves()
        else:
            piece: Piece
            for piece in pieces:
                validMoves.extend(self.validMovesPieceWithChecking(piece))

        self.valid_moves = validMoves

    def guiToBoard(self, pointA, pointB):
        pieceMoved: Piece = self.board[pointA[0]][pointA[1]]
        pieceCaptured: Piece = self.board[pointB[0]][pointB[1]]
        move = Move(pointA, pointB, pieceMoved, pieceCaptured)

        if type(pieceMoved) == Pawn and pieceCaptured == 0 and move.colF != pieceMoved.col:
            direction = 1 if self.playerTurn else -1
            opponentPawn = self.board[move.rowF+direction][move.colF]
            if type(opponentPawn) == Pawn and opponentPawn == self.enPassantPiece:
                move.setPieceCaptured(opponentPawn)


        response = False
        if move in self.valid_moves:
            self.move(move)
            self.updateBoard()
            response = True
        return response, move

  
    def aiToBoard(self, move):
        self.move(move)
        self.updateBoard()

    def setStatus(self):
        if len(self.checks) > 0:
            self.status = CODE_CHECKMATE if len(self.valid_moves) == 0 else CODE_CHECK
            return 
        else:
            self.status = CODE_NORMAL if len(self.valid_moves) > 0 else CODE_STALEMATE

    def getPieceFromSquare(self, square):
        row = square[0]
        col = square[1]
        return self.board[row][col]

    def updateBoard(self):
        self.setValidMoves()
        self.setStatus()
              

if __name__ == '__main__':
    ana = 'ana'
    print(ana[0])
