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
                if not board[y][x] is None:
                    if board[y][x].isWhite == piece.isWhite:
                        movementOptions[y][x] = 0
            elif movementOptions[y][x] == 2:
                if board[y][x] is None:
                    movementOptions[y][x] = 0
                elif board[y][x].isWhite == piece.isWhite:
                    movementOptions[y][x] = 0
                else:
                    movementOptions[y][x] = 1

    movementOptions = checkForBlockedMoves(movementOptions)

    return movementOptions




def checkThatPieceCausesCheck(board, piece):
    availableMoves = piece.getMovableSquares(board)
    for y in range(rows):
        for x in range(cols):
            if availableMoves[y][x] == 1:
                if not board[y][x] is None:
                    if board[y][x].type == 'k' and board[y][x].isWhite != piece.isWhite:
                        return True
    return False


def checkForBlackCausedCheck(board):
    for y in range(rows):
        for x in range(cols):
            if not board[y][x] is None:
                if not board[y][x].isWhite:
                    if checkThatPieceCausesCheck(board, board[y][x]):
                        return True
    return False

def checkForWhiteCausedCheck(board):
    for y in range(rows):
        for x in range(cols):
            if not board[y][x] is None:
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
    newBoard = copy.deepcopy(board)
    newBoard, piece = movePiece(newBoard, piece, movePos)
    if piece.isWhite:
        causedCheck = checkForBlackCausedCheck(newBoard)
    else:
        causedCheck = checkForWhiteCausedCheck(newBoard)

    legal = not causedCheck
    return legal

def moveAchievesCheck(board, piece, movePos):
    newBoard = copy.deepcopy(board)
    newBoard, piece = movePiece(newBoard, piece, movePos)
    if piece.isWhite:
        causedCheck = checkForWhiteCausedCheck(newBoard)
    else:
        causedCheck = checkForBlackCausedCheck(newBoard)

    return causedCheck

def checkIfPieceCanAchieveCheck(board, piece):
    possibleMoves = piece.getMovableAndLegalSquares(copy.deepcopy(board))
    canCheck = False
    for y in range(rows):
        for x in range(cols):
            if possibleMoves[y][x] == 1:
                move = [x, y]
                if moveAchievesCheck(copy.deepcopy(board), copy.deepcopy(piece), move):
                    canCheck = True
    return canCheck

def checkIfWhiteCanCheck(board):
    for y in range(rows):
        for x in range(cols):
            if not board[y][x] is None:
                if board[y][x].isWhite:
                    piece = board[y][x]
                    boardCopy = copy.deepcopy(board)
                    pieceCanCheck = checkIfPieceCanAchieveCheck(boardCopy, copy.deepcopy(piece))
                    if pieceCanCheck:
                        print(board[y][x])
                        print("The piece at position ({X}, {Y}) of type {type} can check.".format(X=x, Y=y, type=piece.type))
                        return True

    return False

class King:
    isWhite = True
    position = [0, 0]
    type = 'k'

    def __init__(self, isWhite, position):
        self.isWhite = isWhite
        self.position = position

    # Returns a vector of all of the move options based on current position
    def movementOptions(self):
        testBoard = np.zeros((rows, cols))
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
        testBoard = np.zeros((rows, cols))
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
        testBoard = np.zeros((rows, cols))
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
        newBoard = board[:]
        movableSquares = self.getMovableSquares(newBoard)
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
        testBoard = np.zeros((rows, cols))
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
        testBoard = np.zeros((rows, cols))
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

        testBoard = np.zeros((rows, cols))
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


def createPiece(x, y, typeChar):
    isWhite = typeChar == typeChar.lower()
    pos = [x, y]

    lowerChar = typeChar.lower()
    if lowerChar == 'k':
        return King(isWhite, pos)
    elif lowerChar == 'q':
        return Queen(isWhite, pos)
    elif lowerChar == 'b':
        return Bishop(isWhite, pos)
    elif lowerChar == 'n':
        return Knight(isWhite, pos)
    elif lowerChar == 'r':
        return Rook(isWhite, pos)
    elif lowerChar == 'p':
        return Pawn(isWhite, pos)
    else:
        print("Error creating piece with char {}.".format(lowerChar))
        exit(-1)

def initialiseBoard():
    board = []
    for y in range(rows):
        row = []
        for x in range(cols):
            row.append(None)
        board.append(row)
    return board

inputFile = "board4.txt"
rows = 5
cols = 5
legalChars = ['K', 'k', 'Q', 'q', 'B', 'b', 'N', 'n', 'R', 'r', 'P', 'p']

f = open(inputFile, 'r')
fLines = f.readlines()
if len(fLines) != rows:
    print("Incorrect number of rows")
    exit(-1)

lines = []
for line in fLines:
    lineStripped = line.strip('\n')
    if len(lineStripped) != cols:
        print("A line had the incorrect number of squares.")
        exit(-1)

    lines.append(lineStripped)


board = initialiseBoard()
for y in range(rows):
    for x in range(cols):
        pieceChar = lines[y][x]
        piece = None
        if pieceChar != '0':
            if not (pieceChar in legalChars):
                print("Illegal character encountered {}.".format(pieceChar))
                exit(-1)
            else:
                piece = createPiece(x, y, pieceChar)
                #print("Created", pieceChar, piece, "at", x, y)
                board[y][x] = piece

#print(checkForWhiteCausedCheck(board))
checkIfWhiteCanCheck(board)
