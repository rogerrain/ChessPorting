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
    def checkValidMoves(self, gs):
        '''
        Returns all valid moves that the piece can make given a GameState gs.
        '''
        pass

class Pawn(Piece):
    def checkValidMoves(self, board):
        validMoves = []
        # White Pawn
        if self.name[0] == "w":
            if board[self.pos[0]-1][self.pos[1]].getName() == "--":
                validMoves.append((self.pos[0]-1, self.pos[1]))
            if self.pos[0] > 0:
                if board[self.pos[0]-1][self.pos[1]-1].getName()[0] == "b":
                    validMoves.append((self.pos[0]-1, self.pos[1]-1))
            if self.pos[0] < 7:
                if board[self.pos[0]-1][self.pos[1]+1].getName()[0] == "b":
                    validMoves.append((self.pos[0]+1, self.pos[1]-1))
            if not self.moved:
                if board[self.pos[0]-2][self.pos[1]].getName() == "--":
                    validMoves.append((self.pos[0]-2, self.pos[1]))
        # Black Pawn
        else:
            if board[self.pos[0]+1][self.pos[1]].getName() == "--":
                validMoves.append((self.pos[0]+1, self.pos[1]))
            if self.pos[0] > 0:
                if board[self.pos[0]+1][self.pos[1]-1].getName()[0] == "w":
                    validMoves.append((self.pos[0]+1, self.pos[1]-1))
            if self.pos[0] < 7:
                if board[self.pos[0]+1][self.pos[1]+1].getName()[0] == "w":
                    validMoves.append((self.pos[0]+1, self.pos[1]+1))
            if not self.moved:
                if board[self.pos[0]+2][self.pos[1]].getName() == "--":
                    validMoves.append((self.pos[0]+2, self.pos[1]))

        return validMoves

class Knight(Piece):
    def checkValidMoves(self, gs):
        validMoves = []
        return validMoves

class Bishop(Piece):
    def checkValidMoves(self, gs):
        validMoves = []
        return validMoves

class Rook(Piece):
    def checkValidMoves(self, gs):
        validMoves = []
        return validMoves

class Queen(Piece):
    def checkValidMoves(self, gs):
        validMoves = []
        return validMoves

class King(Piece):
    def checkValidMoves(self, gs):
        validMoves = []
        return validMoves

# Not an actual chess piece, just an empty space on the board
class Space(Piece):
    def checkValidMoves(self, gs):
        validMoves = []
        return validMoves
