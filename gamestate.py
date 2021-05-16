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
        self.tempVuln = (-1, -1)
        self.vuln = False

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

        for r in range(8):
            for c in range(8):
                self.board[r][c].setPos((r, c))

    def getBoard(self):
        return self.board

    def isVuln(self):
        return self.vuln

    def nextTurn(self):
        self.whiteToMove = not self.whiteToMove

    def whitesTurn(self):
        return self.whiteToMove

    def enableEnPassant(self, pos):
        r = pos[0]
        f = pos[1]
        self.tempVuln = (r, f)
        self.vuln = True
        self.board[r][f] = piece.Space("-e")
        self.board[r][f].setPos((r, f))
        return

    def disableEnPassant(self):
        r = self.tempVuln[0]
        f = self.tempVuln[1]
        if self.board[r][f].getName()[0] == "-":
            self.board[r][f] = piece.Space("--")
            self.board[r][f].setPos((r, f))
        self.tempVuln = (-1, -1)
        self.vuln = False
        return

    def enPassant(self):
        if self.whiteToMove:
            direction = 1
        else:
            direction = -1
        r = self.tempVuln[0] + direction
        f = self.tempVuln[1]
        self.board[r][f] = piece.Space("--")
        self.board[r][f].setPos((r, f))

    def updateBoard(self, p1, p2):
        '''
        Moves the piece p1 to the position of piece p2 and deletes p2
            Piece p1: The active piece which is moving
            Piece p2: The piece being replaced
        '''
        pos1 = p1.getPos()
        pos2 = p2.getPos()
        p2 = None
        self.board[pos2[0]][pos2[1]] = p1
        p1.setPos(pos2)
        p1.move()
        self.board[pos1[0]][pos1[1]] = piece.Space("--")
        self.board[pos1[0]][pos1[1]].setPos(pos1)
        return