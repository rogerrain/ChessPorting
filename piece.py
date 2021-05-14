from abc import ABC, abstractmethod

class Piece(ABC):
    def __init__(self, name):
        '''
        Data structure for a generic Chess Piece
            string name:    A two-letter string where the first letter represents 
                            the colour and the second represents the type of piece.
                            e.g. "wB" = "White Bishop," "bQ" = "Black Queen."
                            Empty spaces are given the name "--"
        '''
        self.name = name
        self.colour = name[0]
        self.moved = False  # Whether or not the piece has been moved yet
        self.pos = (-1, -1)

    def getName(self):
        return self.name

    def getColour(self):
        return self.colour

    def move(self):
        self.moved = True
        return

    def setPos(self, r, c):
        self.pos = (r, c)
        return

    @abstractmethod
    def checkValidMoves(self, board):
        '''
        Returns all valid moves that the piece can make given the game board
        '''
        pass

def checkDiagonals(r, f, colour, board):
    '''
    Helper function for checking the possible diagonal moves of a piece
        Int r: The piece's corresponding rank on the board
        Int f: The piece's corresponding file on the board
        String colour: A letter corresponding to the piece's colour
        List board: A list of lists of pieces, each corresponding to a rank
    '''
    diagonalMoves = []
    b = 7 - r # Number of rows below the piece
    a = 7 - b # Number of rows above the piece
    # Checking diagonally down-right
    for i in range(b):
        if 1 <= (r+i+1) <= 7 and 1 <= (f+i+1) <= 7:
            c = board[r+i+1][f+i+1].getColour()
            if c != colour:
                diagonalMoves.append((r+i+1, f+i+1))
                if c != "-":
                    break
            else:
                break
        else:
            break
    # Checking diagonally down-left
    for i in range(b):
        if 1 <= (r+i+1) <= 7 and 0 <= (f-i-1) <= 6:
            c = board[r+i+1][f-i-1].getColour()
            if c != colour:
                diagonalMoves.append((r+i+1, f-i-1))
                if c != "-":
                    break
            else: 
                break
        else:
            break
    # Checking diagonally up-right
    for i in range(a):
        if 0 <= (r-i-1) <= 6 and 1 <= (f+i+1) <= 7:
            c = board[r-i-1][f+i+1].getColour()
            if c != colour:
                diagonalMoves.append((r-i-1, f+i+1))
                if c != "-":
                    break
            else: 
                break
        else:
            break
    # Checking diagonally up-left
    for i in range(a):
        if 0 <= (r-i-1) <= 6 and 0 <= (f-i-1) <= 6:
            c = board[r-i-1][f-i-1].getColour()
            if c != colour:
                diagonalMoves.append((r-i-1, f-i-1))
                if c != "-":
                    break
            else:
                break
        else:
            break

    return diagonalMoves

def checkStraights(r, f, colour, board):
    '''
    Helper function for checking the possible straight moves of a piece
        Int r: The piece's corresponding rank on the board
        Int f: The piece's corresponding file on the board
        String colour: A letter corresponding to the piece's colour
        List board: A list of lists of pieces, each corresponding to a rank
    '''
    straightMoves = []
    # Checking upwards in the file
    for i in range(r-1, -1, -1):
        c = board[i][f].getColour()
        if c != colour:
            straightMoves.append((i, f))
            if c != "-":
                break
        else:
            break
    # Checking downwards in the file
    for i in range(r, 7):
        c = board[i][f].getColour()
        if c != colour:
            straightMoves.append((i, f))
            if c != "-":
                break
        else:
            break
    # Checking to the left in the rank
    for i in range(f-1, -1, -1):
        c = board[r][i].getColour()
        if c != colour:
            straightMoves.append((r, i))
            if c != "-":
                break
        else:
            break
    # Checking to the right in the rank
    for i in range(f, 7):
        c = board[r][i].getColour()
        if c != colour:
            straightMoves.append((r, i))
            if c != "-":
                break
        else:
            break 
    return straightMoves

class Pawn(Piece):
    def checkValidMoves(self, board):
        validMoves = []
        # White Pawn
        if self.colour == "w":
            if board[self.pos[0]-1][self.pos[1]].getName() == "--":
                validMoves.append((self.pos[0]-1, self.pos[1]))
            if self.pos[1] > 0:
                if board[self.pos[0]-1][self.pos[1]-1].getColour() == "b":
                    validMoves.append((self.pos[0]-1, self.pos[1]-1))
            if self.pos[1] < 7:
                if board[self.pos[0]-1][self.pos[1]+1].getColour() == "b":
                    validMoves.append((self.pos[0]+1, self.pos[1]-1))
            if not self.moved:
                if board[self.pos[0]-2][self.pos[1]].getName() == "--":
                    validMoves.append((self.pos[0]-2, self.pos[1]))
        # Black Pawn
        else:
            if board[self.pos[0]+1][self.pos[1]].getName() == "--":
                validMoves.append((self.pos[0]+1, self.pos[1]))
            if self.pos[1] > 0:
                if board[self.pos[0]+1][self.pos[1]-1].getColour() == "w":
                    validMoves.append((self.pos[0]+1, self.pos[1]-1))
            if self.pos[1] < 7:
                if board[self.pos[0]+1][self.pos[1]+1].getColour() == "w":
                    validMoves.append((self.pos[0]+1, self.pos[1]+1))
            if not self.moved:
                if board[self.pos[0]+2][self.pos[1]].getName() == "--":
                    validMoves.append((self.pos[0]+2, self.pos[1]))

        return validMoves

class Knight(Piece):
    def checkValidMoves(self, board):
        validMoves = []
        possibleMoves = []
        r = self.pos[0]
        f = self.pos[1]
        possibleMoves.append((r-2, f-1))
        possibleMoves.append((r-2, f+1))
        possibleMoves.append((r-1, f-2))
        possibleMoves.append((r-1, f+2))
        possibleMoves.append((r+1, f-2))
        possibleMoves.append((r+1, f+2))
        possibleMoves.append((r+2, f-1))
        possibleMoves.append((r+2, f+1))
        for move in possibleMoves:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                if board[move[0]][move[1]].getColour() != self.colour:
                    validMoves.append(move)

        return validMoves

class Bishop(Piece):
    def checkValidMoves(self, board):
        r = self.pos[0]
        f = self.pos[1]
        return checkDiagonals(r, f, self.colour, board)


class Rook(Piece):
    def checkValidMoves(self, board):
        r = self.pos[0]
        f = self.pos[1]
        return checkStraights(r, f, self.colour, board)

class Queen(Piece):
    def checkValidMoves(self, board):
        r = self.pos[0]
        f = self.pos[1]
        diagonals = checkDiagonals(r, f, self.colour, board)
        straights = checkStraights(r, f, self.colour, board)
        return diagonals + straights

class King(Piece):
    def checkValidMoves(self, board):
        validMoves = []
        r = self.pos[0]
        f = self.pos[1]
        possibleMoves = []
        possibleMoves.append((r-1, f-1))
        possibleMoves.append((r-1, f))
        possibleMoves.append((r-1, f+1))
        possibleMoves.append((r, f+1))
        possibleMoves.append((r+1, f+1))
        possibleMoves.append((r+1, f))
        possibleMoves.append((r+1, f-1))
        possibleMoves.append((r, f-1))
        for move in possibleMoves:
            if 0 <= move[0] <= 7 and 0 <= move[1] <= 7:
                if board[move[0]][move[1]].getColour() != self.colour:
                    validMoves.append(move)

        return validMoves

# Not an actual chess piece, just an empty space on the board
class Space(Piece):
    def checkValidMoves(self, board):
        return []
