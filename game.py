import pygame as pg
import os
from gamestate import GameState

#Globals
WIDTH = 720
HEIGHT = 720
SQ_SIZE = HEIGHT // 8
MAX_FPS = 60

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
        Surface screen: The display window for the application
        List board: A list of lists of pieces, each referring to a rank
        Dict images: A dictionary containing path locations for images
    '''
    for r in range(len(board)):
        for c in range(len(board)):
            name = board[r][c].getName()
            if name != "--":
                screen.blit(images[name], pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawBoard(screen, colours):
    '''
    Draws the background of the chess board
        Surface screen: The display window for the application
        List colours: A list of colours used for the light and dark squares
    '''
    for r in range(8):
        for c in range(8):
            colour = colours[((c + r) % 2)]
            pg.draw.rect(screen, colour, pg.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    return

def squareDict(order, whitePOV):
    '''
    Returns a dictionary that converts window positions to rank or file names
        string order: The characters that each rank or file will be named
        Bool whitePOV: The orientation of the board on the window
    '''
    sd = {}
    if not whitePOV:
        order = order[::-1]

    for item in enumerate(order):
        sd[item[0]] = item[1]
    
    return sd


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

    images = loadImages()
    drawBoard(screen, colours)

    # Event Loop
    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False

            elif e.type == pg.MOUSEBUTTONDOWN:
                print("position: {a} ({c}{b})".format(a=e.pos, 
                    b=rd[(e.pos[1]//SQ_SIZE)], c=fd[(e.pos[0]//SQ_SIZE)]))
                rank = e.pos[1] // SQ_SIZE
                file = e.pos[0] // SQ_SIZE

        drawBoard(screen, colours)
        drawPieces(screen, gs.getBoard(), images)
        clock.tick(MAX_FPS)
        pg.display.flip()

    return

if __name__ == "__main__":
    main()
