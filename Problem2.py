import numpy as np
import copy

def getNeighbouringCells(position):
    coords = []
    for y in range(rows):
        for x in range(cols):
            xDist = x - position[0]
            yDist = y - position[1]
            if xDist + yDist != 0 and (xDist <= 1 and yDist <= 1):
                coords.append([x, y])
    return coords

def checkForBlockedMoves(movementOptions):
    for y in range(rows):
        for x in range(cols):
            if movementOptions[y][x] == 1:
                neighbouringCells = getNeighbouringCells([x, y])
                found = False
                for coord in neighbouringCells:
                    if movementOptions[coord[1]][coord[0]] == 1:
                        found = True
                if not found:
                    movementOptions[y][x] = 0
    return movementOptions


def nonCollisionMoves(board, piece):
    movementOptions = piece.movementOptions()

    for y in range(rows):
        for x in range(cols):
            if movementOptions[y][x] == 1:
                if board[y][x] != None:
                    if board[y][x].isWhite == piece.isWhite:
                        movementOptions[y][x] = 0
            elif movementOptions[y][x] == 2:
                if board[y][x] == None:
                    movementOptions[y][x] = 0
                elif board[y][x].isWhite == piece.isWhite:
                    movementOptions[y][x] = 0
                else:
                    movementOptions[y][x] = 1

    movementOptions = checkForBlockedMoves(movementOptions)

    return movementOptions




def checkThatPieceCausesCheck(board, piece):
    availableMoves = piece.getMovableSquares()
    for y in range(rows):
        for x in range(cols):
            if availableMoves[y][x] == 1:
                if board[y][x].type == 'k' and board[y][x].isWhite != piece.isWhite:
                    return True
    return False


def checkForBlackCausedCheck(board):
    for y in range(rows):
        for x in range(cols):
            if not board[y][x].isWhite:
                if checkThatPieceCausesCheck(board, board[y][x]):
                    return True
    return False

def checkForWhiteCausedCheck(board):
    for y in range(rows):
        for x in range(cols):
            if board[y][x].isWhite:
                if checkThatPieceCausesCheck(board, board[y][x]):
                    return True
    return False

def movePiece(board, piece, position):
    currentPos = piece.position
    piece.position = position
    board[position[1]][position[0]] = piece
    board[currentPos[1]][currentPos[0]] = None

    return board, piece


def checkMoveIsLegal(board, piece, movePos):
    newBoard = copy.copy(board)
    newBoard, piece = movePiece(newBoard, piece, movePos)
    if piece.isWhite:
        causedCheck = checkForBlackCausedCheck(newBoard)
    else:
        causedCheck = checkForWhiteCausedCheck(newBoard)

    legal = not causedCheck
    return legal

class King:
    isWhite = True
    position = [0, 0]
    type = 'k'

    def __init__(self, isWhite, position):
        self.isWhite = isWhite
        self.position = position

    # Returns a vector of all of the move options based on current position
    def movementOptions(self):
        testBoard = np.zeros(rows, cols)
        for y in range(rows):
            for x in range(cols):
                xRel = x - self.position[0]
                yRel = y - self.position[1]

                if (np.abs(xRel) == 1 or np.abs(yRel) == 1) and (np.abs(xRel) <= 1 and np.abs(yRel) <= 1):
                    testBoard[y][x] = 1
        return testBoard

    def getMovableSquares(self, board):
        movementOptions = nonCollisionMoves(board, self)
        return movementOptions

    def getMovableAndLegalSquares(self, board):
        movableSquares = self.getMovableSquares(board)
        for y in range(rows):
            for x in range(cols):
                if movableSquares[y][x] == 1:
                    pos = [x, y]
                    isLegal = checkMoveIsLegal(board, self, pos)

                    if not isLegal:
                        movableSquares[y][x] = 0
        return movableSquares
    #penis

class Queen:
    isWhite = True
    position = [0, 0]
    type = 'q'

    def __init__(self, isWhite, position):
        self.isWhite = isWhite
        self.position = position

    # Returns a vector of all of the move options based on current position
    def movementOptions(self):
        testBoard = np.zeros(rows, cols)
        for y in range(rows):
            for x in range(cols):
                xRel = x - self.position[0]
                yRel = y - self.position[1]

                if np.abs(xRel) == 1 or np.abs(yRel) == 1:
                    testBoard[y][x] = 1
        return testBoard

    def getMovableSquares(self, board):
        movementOptions = nonCollisionMoves(board, self)
        return movementOptions

    def getMovableAndLegalSquares(self, board):
        movableSquares = self.getMovableSquares(board)
        for y in range(rows):
            for x in range(cols):
                if movableSquares[y][x] == 1:
                    pos = [x, y]
                    isLegal = checkMoveIsLegal(board, self, pos)

                    if not isLegal:
                        movableSquares[y][x] = 0
        return movableSquares

class Bishop:
    isWhite = True
    position = [0, 0]
    type = 'b'

    def __init__(self, isWhite, position):
        self.isWhite = isWhite
        self.position = position

    # Returns a vector of all of the move options based on current position
    def movementOptions(self):
        testBoard = np.zeros(rows, cols)
        for y in range(rows):
            for x in range(cols):
                xRel = x - self.position[0]
                yRel = y - self.position[1]

                if np.abs(xRel) == np.abs(yRel):
                    testBoard[y][x] = 1
        return testBoard

    def getMovableSquares(self, board):
        movementOptions = nonCollisionMoves(board, self)
        return movementOptions

    def getMovableAndLegalSquares(self, board):
        movableSquares = self.getMovableSquares(board)
        for y in range(rows):
            for x in range(cols):
                if movableSquares[y][x] == 1:
                    pos = [x, y]
                    isLegal = checkMoveIsLegal(board, self, pos)

                    if not isLegal:
                        movableSquares[y][x] = 0
        return movableSquares


class Knight:
    isWhite = True
    position = [0, 0]
    type = 'n'

    def __init__(self, isWhite, position):
        self.isWhite = isWhite
        self.position = position

    # Returns a vector of all of the move options based on current position
    def movementOptions(self):
        testBoard = np.zeros(rows, cols)
        for y in range(rows):
            for x in range(cols):
                xRel = x - self.position[0]
                yRel = y - self.position[1]

                if (np.abs(xRel) == 3 or np.abs(yRel) == 3) and np.abs(xRel) + np.abs(yRel) == 4:
                    testBoard[y][x] = 1
        return testBoard

    def getMovableSquares(self, board):
        movementOptions = nonCollisionMoves(board, self)
        return movementOptions

    def getMovableAndLegalSquares(self, board):
        movableSquares = self.getMovableSquares(board)
        for y in range(rows):
            for x in range(cols):
                if movableSquares[y][x] == 1:
                    pos = [x, y]
                    isLegal = checkMoveIsLegal(board, self, pos)

                    if not isLegal:
                        movableSquares[y][x] = 0
        return movableSquares


class Rook:
    isWhite = True
    position = [0, 0]
    type = 'r'

    def __init__(self, isWhite, position):
        self.isWhite = isWhite
        self.position = position

    # Returns a vector of all of the move options based on current position
    def movementOptions(self):
        testBoard = np.zeros(rows, cols)
        for y in range(rows):
            for x in range(cols):
                xRel = x - self.position[0]
                yRel = y - self.position[1]

                if np.abs(xRel) == 0 or np.abs(yRel) == 0:
                    testBoard[y][x] = 1
        return testBoard

    def getMovableSquares(self, board):
        movementOptions = nonCollisionMoves(board, self)
        return movementOptions

    def getMovableAndLegalSquares(self, board):
        movableSquares = self.getMovableSquares(board)
        for y in range(rows):
            for x in range(cols):
                if movableSquares[y][x] == 1:
                    pos = [x, y]
                    isLegal = checkMoveIsLegal(board, self, pos)

                    if not isLegal:
                        movableSquares[y][x] = 0
        return movableSquares

class Pawn:
    isWhite = True
    position = [0, 0]
    type = 'p'

    def __init__(self, isWhite, position):
        self.isWhite = isWhite
        self.position = position

    # Returns a vector of all of the move options based on current position
    def movementOptions(self):
        if self.isWhite:
            dir = 1
        else:
            dir = -1

        testBoard = np.zeros(rows, cols)
        for y in range(rows):
            for x in range(cols):
                xRel = x - self.position[0]
                yRel = y - self.position[1]

                if np.abs(xRel) == 1 and yRel == dir:
                    testBoard[y][x] = 2
                elif np.abs(xRel) == 0 and yRel == dir:
                    testBoard[y][x] = 1
        return testBoard
    # thanks for all your help <3 penis

    def getMovableSquares(self, board):
        movementOptions = nonCollisionMoves(board, self)
        return movementOptions

    def getMovableAndLegalSquares(self, board):
        movableSquares = self.getMovableSquares(board)
        for y in range(rows):
            for x in range(cols):
                if movableSquares[y][x] == 1:
                    pos = [x, y]
                    isLegal = checkMoveIsLegal(board, self, pos)

                    if not isLegal:
                        movableSquares[y][x] = 0
        return movableSquares





inputFile = "board1.txt"
rows = 5
cols = 5

f = open(inputFile, 'r')
fLines = f.readlines()
if len(fLines) != rows:
    print("Incorrect number of rows")
    exit(-1)

lines = []
for line in fLines:
    lineStripped = line.strip('\n')
    if len(lineStripped) != cols:
        print("A line had the incorect number of squares.")
        exit(-1)

    lines.append(lineStripped)





