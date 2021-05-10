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

    def getName(self):
        return self.name

    def getColour(self):
        return self.colour

    @abstractmethod
    def checkValidMoves(self, gs):
        '''
        Returns all valid moves that the piece can make given a GameState gs.
        '''
        pass

class Pawn(Piece):
    def checkValidMoves(self, gs):
        pass

class Knight(Piece):
    def checkValidMoves(self, gs):
        pass

class Bishop(Piece):
    def checkValidMoves(self, gs):
        pass

class Rook(Piece):
    def checkValidMoves(self, gs):
        pass

class Queen(Piece):
    def checkValidMoves(self, gs):
        pass

class King(Piece):
    def checkValidMoves(self, gs):
        pass

# Not an actual chess piece, just an empty space on the board
class Space(Piece):
    def checkValidMoves(self, gs):
        pass
