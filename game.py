import pygame as pg
from gamestate import GameState

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
                screen.blit(images[name], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

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
    screen.blit(images[name], pg.Rect((x-(SQ_SIZE//2)), (y-(SQ_SIZE//2)), SQ_SIZE, SQ_SIZE))
    return

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
    # Checking if move is an En Passant
    if activePiece.getName()[1] == "p" and gs.getBoard()[newpos[0]][newpos[1]].getName()[1] == "e":
        gs.enPassant()

    # Forgetting previous En Passant vulnerabilities
    if gs.isVuln():
        gs.disableEnPassant()

    # Setting up En Passants if applicable
    if activePiece.getName()[1] == "p" and not activePiece.hasMoved():
        if ((activePiece.getPos()[1] - newpos[1]) % 2) == 0: # If the pawn moved two squares
            if activePiece.getColour() == "w":
                gs.enableEnPassant((newpos[0]+1, newpos[1]))
            else:
                gs.enableEnPassant((newpos[0]-1, newpos[1]))

    # Normal board update
    gs.updateBoard(activePiece, gs.getBoard()[newpos[0]][newpos[1]])
    gs.nextTurn()
    return gs

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
    activeValidMoves = []
    xpos = 0
    ypos = 0

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

                    if not pieceActive:
                        if (gs.whitesTurn() and gs.getBoard()[rank][file].getColour() == "w") or \
                        (not gs.whitesTurn() and gs.getBoard()[rank][file].getColour() == "b"):
                            pieceActive = True
                            activePiece = gs.getBoard()[rank][file]
                            activeValidMoves = activePiece.checkValidMoves(gs.getBoard())
                            print(activeValidMoves)
                        else:
                            pieceActive = False
                    else:
                        if (rank, file) in activeValidMoves:
                            gs = movePiece(gs, activePiece, (rank, file))
                        pieceActive = False
                        activePiece = None
                        
                elif e.button == 3: #Right Mouse Button
                    holdingRMB = True
                    pieceActive = False
                    activePiece = None

            elif e.type == pg.MOUSEBUTTONUP:
                if e.button == 1:
                    holdingLMB = False
                    uprank = e.pos[1]//SQ_SIZE
                    upfile = e.pos[0]//SQ_SIZE
                    if rank == uprank and file == upfile:
                        print("same square")
                    else:
                        print("Moved from {a}{b} to {c}{d}".format(a=fd[file], 
                            b=rd[rank], c=fd[upfile], d=rd[uprank]))
                        if pieceActive and (uprank, upfile) in activeValidMoves:
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
