import pygame as pg
# from pygame.math import enable_swizzling
from gamestate import GameState
import copy

#Globals
WIDTH = 720
HEIGHT = 720
SQ_SIZE = HEIGHT // 8
MAX_FPS = 120

#Load resources
def loadImages():
    images = {} #Dictionary of images with 2-character keys
    pieces = ["R", "N", "B", "Q", "K", "p"]
    dir = "./Pieces/"
    for piece in pieces:
        w = "w" + piece
        b = "b" + piece
        images[w] = pg.transform.scale(pg.image.load(dir + w + ".png"), (SQ_SIZE, SQ_SIZE))
        images[b] = pg.transform.scale(pg.image.load(dir + b + ".png"), (SQ_SIZE, SQ_SIZE))

    return images

def changeTheme(n):
    '''
    Changes the list of colours depending on the number given
        Int n: A number corresponding to the colour theme requested
    '''
    colourThemes = [
        [pg.Color(240, 217, 181), pg.Color(181, 136, 99)],  #Lichess
        [pg.Color(235, 236, 208), pg.Color(119, 149, 86)],  #Chess.com
        [pg.Color(102, 136, 204), pg.Color(5, 19, 54)],     #Abyss
        [pg.Color("white"), pg.Color("gray")]               #Black-and-White
        ]

    return colourThemes[n-1]

def drawPieces(screen, board, images):
    '''
    Draws the chess pieces
        pygame.Surface screen: The display window for the application
        List board: A list of lists of pieces, each corresponding to a rank
        Dict images: A dictionary containing path locations for images
    '''
    for r in range(len(board)):
        for c in range(len(board)):
            name = board[r][c].getName()
            if name[0] != "-":
                screen.blit(images[name], (c*SQ_SIZE, r*SQ_SIZE))

    return

def drawBoard(screen, colours):
    '''
    Draws the background of the chess board
        pygame.Surface screen: The display window for the application
        List colours: A list of colours used for the light and dark squares
    '''
    for r in range(8):
        for c in range(8):
            colour = colours[((c + r) % 2)]
            pg.draw.rect(screen, colour, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    return

def drawGhost(screen, rank, file):
    '''
    Draws a translucent white square above the piece being held
        pygame.Surface screen: The display window for the application
        Int rank: Corresponds to the rank of the piece on the board minus 1
        Int file: Corresponds to the file of the piece on the board minus 1
    '''
    whiteSquare = pg.Surface((SQ_SIZE, SQ_SIZE))
    whiteSquare.set_alpha(128)
    whiteSquare.fill((255, 255, 255))
    screen.blit(whiteSquare, (file*SQ_SIZE, rank*SQ_SIZE))
    return

def drawValidMoves(screen, moves):
    '''
    Draws a circle on all squares where the active piece can move to
        pygame.Surface screen: The display window for the application
        List moves: A list of tuples corresponding to the valid moves
    '''
    for move in moves:
        m = (move[1]*SQ_SIZE + (SQ_SIZE // 2), move[0]*SQ_SIZE + (SQ_SIZE // 2))
        pg.draw.circle(screen, pg.Color("green"), m, SQ_SIZE//6)
    return

def pieceFollowMouse(screen, name, images, x, y):
    '''
    Draws the active piece at the position of the mouse while LMB is held
        pygame.Surface screen: The display window for the application
        string Name: The 2-character name of the active piece
        Dict images: A dictionary containing path locations for images
        Int x: The x-position of the mouse on the screen
        Int y: The y-position of the mouse on the screen
    '''
    screen.blit(images[name], (x-(SQ_SIZE//2), (y-(SQ_SIZE//2))))
    return

def drawPromotionChoices(screen, promotionSquare, images):
    '''
    Draws the choices for promotion onto the screen
        pygame.Surface screen: The display window for the application
        Tuple promotionSquare: The square that the promoted pawn will end up at
        Dict images: A dictionary containing path locations for images
    '''
    r = promotionSquare[0]
    f = promotionSquare[1]
    pieces = ["Q", "N", "R", "B"]
    promotionOptions = []

    fade = pg.Surface((WIDTH, HEIGHT))
    fade.set_alpha(150)
    fade.fill((255, 255, 255))
    screen.blit(fade, (0, 0))

    if r == 0:  # A white pawn is promoting
        for i in range(4):
            name = "w" + pieces[i]
            m = (f*SQ_SIZE + (SQ_SIZE // 2), i*SQ_SIZE + (SQ_SIZE // 2))
            pg.draw.circle(screen, pg.Color("gray"), m, SQ_SIZE // 2)
            screen.blit(images[name], (f*SQ_SIZE, i*SQ_SIZE))
            promotionOptions.append((i, f))
    else:       # A black pawn is promoting
        for i in range(4):
            name = "b" + pieces[i]
            m = (f*SQ_SIZE + (SQ_SIZE // 2), (7-i)*SQ_SIZE + (SQ_SIZE // 2))
            pg.draw.circle(screen, pg.Color("gray"), m, SQ_SIZE // 2)
            screen.blit(images[name], (f*SQ_SIZE, (7-i)*SQ_SIZE))
            promotionOptions.append((7-i, f))

    return promotionOptions

def squareDict(order, whitePOV):
    '''
    Returns a dictionary for converting window positions to rank or file names
        String order: The characters that each rank or file will be named
        Bool whitePOV: The orientation of the board on the window
    '''
    sd = {}
    if not whitePOV:
        order = order[::-1]

    for item in enumerate(order):
        sd[item[0]] = item[1]
    
    return sd

def movePiece(gs, activePiece, newpos):
    '''
    Moves the active piece to the specified new position on the board
        GameState gs: The current Game State object
        Piece activePiece: The piece which is moving to a new position
        Tuple newpos: The position to which the active piece is moving
    '''
    activeType = activePiece.getName()[1]

    # Checking if move is an En Passant
    if activeType == "p" and gs.getBoard()[newpos[0]][newpos[1]].getName()[1] == "e":
        gs.enPassant()

    # Forgetting previous En Passant vulnerabilities
    if gs.isVuln():
        gs.disableEnPassant()

    # Setting up En Passants if applicable
    if activeType == "p" and not activePiece.hasMoved():
        if ((activePiece.getPos()[1] - newpos[1]) % 2) == 0: # If the pawn moved two squares
            if activePiece.getColour() == "w":
                gs.enableEnPassant((newpos[0]+1, newpos[1]))
            else:
                gs.enableEnPassant((newpos[0]-1, newpos[1]))

    #Checking for castling
    if activeType == "K" and not activePiece.hasMoved():
        if newpos[1] in [2, 6]:
            gs.castle(activePiece.getColour(), newpos[1])

    # Normal board update
    gs.updateBoard(activePiece, gs.getBoard()[newpos[0]][newpos[1]])
    gs.nextTurn()
    return gs

def promotePawn(gs, activePiece, promotionSquare, rank):
    '''
    Promoting the active pawn to a piece determined by the rank
        GameState gs: The current Game State object
        Piece activePiece: The piece which is being promoted
    '''
    r = activePiece.getPos()[0]
    f = activePiece.getPos()[1]
    colour = activePiece.getColour()
    if rank in [0, 7]:
        t = "Q"
    elif rank in [1, 6]:
        t = "N"
    elif rank in [2, 5]:
        t = "R"
    else:
        t = "B"
    name = colour + t
    gs.promote(activePiece, name)
    gs = movePiece(gs, gs.getBoard()[r][f], promotionSquare)

    return gs

def checkKingSafety(gs, colour, activepos, newpos):
    '''
    Checks whether or not the given move would leave the player's king immediately vulnerable
        GameState gs: The current Game State object
        String colour: The colour of the player whose turn it is
        Tuple activepos: The current position of the piece being moved
        Tuple newpos: The new position of the active piece if the move is played
    '''
    ts = copy.deepcopy(gs)
    ts = movePiece(ts, ts.getBoard()[activepos[0]][activepos[1]], newpos)
    
    return not ts.inCheck(colour)

def filterValidMoves(gs, activePiece, moves):
    '''
    Given a list of moves, returns all moves where the king is not under attack
        GameState gs: The current Game State object
        Piece activePiece: The piece whose moves are being validated
        List moves: The moves to check the validity of
    '''
    activePos = (activePiece.getPos())
    colour = activePiece.getColour()
    safeMoves = []
    for move in moves:
        if checkKingSafety(gs, colour, activePos, move):
            safeMoves.append(move)

    # Check for castling while in check
    if activePiece.getName()[1] == "K" and not activePiece.hasMoved():
        if gs.inCheck(colour):
            safeMoves = [m for m in safeMoves if m[1] not in [2, 6]]

    return safeMoves

def gameStatus(gs):
    pass

def main():
    #Initialize the game
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Python Chess")
    clock = pg.time.Clock()
    colours = changeTheme(1) #Default Colour Theme
    gs = GameState()
    gs.makeDefaultBoard()

    # Creating a dictionary for squares based on the position on the window
    ranks = "87654321"
    files = "abcdefgh"
    rd = squareDict(ranks, True)
    fd = squareDict(files, True)

    # Keeping track of the file and rank when the mouse is clicked or released
    rank = -1
    file = -1
    uprank = -1
    upfile = -1

    # Variables to keep track of whether the mouse buttons are being held
    holdingLMB = False
    holdingRMB = False

    pieceActive = False
    activePiece = None
    activePossibleMoves = []
    activeValidMoves = []
    xpos = 0
    ypos = 0
    promoting = False
    promotionSquare = (-1, -1)
    promotionOptions = []
    clickedWhilePromoting = False

    images = loadImages()
    drawBoard(screen, colours)

    # Event Loop
    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

            elif e.type == pg.MOUSEBUTTONDOWN:
                if e.button == 1:   #Left Mouse Button
                    holdingLMB = True
                    xpos = e.pos[0]
                    ypos = e.pos[1]
                    rank = ypos // SQ_SIZE
                    file = xpos // SQ_SIZE
                    print("position: {a} ({b}{c}), button: {d}".format(a=e.pos, 
                        b=fd[file], c=rd[rank], d=e.button))

                    # Making sure the player left clicks the piece they want to promote to
                    clickedWhilePromoting = promoting

                    if not pieceActive:
                        if (gs.whitesTurn() and gs.getBoard()[rank][file].getColour() == "w") or \
                        (not gs.whitesTurn() and gs.getBoard()[rank][file].getColour() == "b"):
                            pieceActive = True
                            activePiece = gs.getBoard()[rank][file]
                            activePossibleMoves = activePiece.checkValidMoves(gs.getBoard())
                            activeValidMoves = filterValidMoves(gs, activePiece, activePossibleMoves)
                            print(activeValidMoves)
                        else:
                            pieceActive = False
                    else:
                        if (rank, file) in activeValidMoves:
                            # Check for a promoting pawn
                            if activePiece.getName()[1] == "p" and rank in [0, 7]:
                                promoting = True
                                activeValidMoves = []
                                promotionSquare = (rank, file)
                            else:
                                gs = movePiece(gs, activePiece, (rank, file))
                        if not promoting:
                            pieceActive = False
                            activePiece = None
                        
                elif e.button == 3: # Right Mouse Button
                    holdingRMB = True
                    pieceActive = False
                    activePiece = None

            elif e.type == pg.MOUSEBUTTONUP:
                if e.button == 1:
                    holdingLMB = False
                    uprank = e.pos[1]//SQ_SIZE
                    upfile = e.pos[0]//SQ_SIZE
                    if rank == uprank and file == upfile:
                        # Same square was pressed and released
                        if promoting and clickedWhilePromoting:
                            if (rank, file) in promotionOptions:
                                gs = promotePawn(gs, activePiece, promotionSquare, rank)
                            promoting = False
                            promotionSquare = (-1, -1)
                            pieceActive = False
                            activePiece = None
                    else:
                        print("Moved from {a}{b} to {c}{d}".format(a=fd[file], 
                            b=rd[rank], c=fd[upfile], d=rd[uprank]))
                        if promoting:
                            promoting = False
                            promotionSquare = (-1, -1)
                            pieceActive = False
                            activePiece = None
                        else:
                            if pieceActive and (uprank, upfile) in activeValidMoves:
                                # Check for a promoting pawn
                                if activePiece.getName()[1] == "p" and uprank in [0, 7]:
                                    promoting = True
                                    activeValidMoves = []
                                    promotionSquare = (uprank, upfile)
                                else:
                                    gs = movePiece(gs, activePiece, (uprank, upfile))
                                    pieceActive = False
                                    activePiece = None

                elif e.button == 3:
                    holdingRMB = False

            elif e.type == pg.MOUSEMOTION:
                xpos = e.pos[0]
                ypos = e.pos[1]
                
        # Draw the board and pieces
        drawBoard(screen, colours)
        drawPieces(screen, gs.getBoard(), images)

        # Draw extra things on top of those
        if pieceActive:
            if promoting:
                promotionOptions = drawPromotionChoices(screen, promotionSquare, images)
            else:
                drawGhost(screen, rank, file)
                drawValidMoves(screen, activeValidMoves)
                name = gs.getBoard()[rank][file].getName()
                if holdingLMB:
                    pieceFollowMouse(screen, name, images, xpos, ypos)
                else:
                    screen.blit(images[name], pg.Rect(file*SQ_SIZE, rank*SQ_SIZE, SQ_SIZE, SQ_SIZE))

        clock.tick(MAX_FPS)
        pg.display.flip()

    return

if __name__ == "__main__":
    main()
