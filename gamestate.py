import piece

def makePiece(name):
    if name[1] == "p":
        return piece.Pawn(name)
    elif name[1] == "N":
        return piece.Knight(name)
    elif name[1] == "B":
        return piece.Bishop(name)
    elif name[1] == "R":
        return piece.Rook(name)
    elif name[1] == "Q":
        return piece.Queen(name)
    elif name[1] == "K":
        return piece.King(name)
    else:
        return piece.Space("--")

class GameState:

    def __init__(self):
        self.board = []         #List of Pieces
        self.whiteToMove = True

    def makeDefaultBoard(self):
        default = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]

        self.board = []
        for rank in default:
            self.board.append([makePiece(name) for name in rank])

    def getBoard(self):
        return self.board

    def nextTurn(self):
        self.whiteToMove = not self.whiteToMove

    def whitesTurn(self):
        return self.whiteToMove
        