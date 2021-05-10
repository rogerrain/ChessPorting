import pygame as pg
import os
from gamestate import GameState

#Globals
WIDTH = 480
HEIGHT = 480
TILE_SIZE = HEIGHT // 8
MAX_FPS = 60

#Load resources
def loadImages():
    images = {} #Dictionary of images with 2-character keys
    pieces = ["R", "N", "B", "Q", "K", "p"]
    dir = "./Pieces/"
    for piece in pieces:
        w = "w" + piece
        b = "b" + piece
        images[w] = pg.transform.scale(pg.image.load(dir + w + ".png"), (TILE_SIZE, TILE_SIZE))
        images[b] = pg.transform.scale(pg.image.load(dir + b + ".png"), (TILE_SIZE, TILE_SIZE))

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
                screen.blit(images[name], pg.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))

def drawBoard(screen, colours):
    '''
    Draws the background of the chess board
        Surface screen: The display window for the application
        List colours: A list of colours used for the light and dark squares
    '''
    for r in range(8):
        for c in range(8):
            colour = colours[((c + r) % 2)]
            pg.draw.rect(screen, colour, pg.Rect(c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))
    return

def main():
    #Initialize the game
    pg.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption("Python Chess")
    clock = pg.time.Clock()
    colours = changeTheme(1) #Default Colour Theme
    gs = GameState()
    gs.makeDefaultBoard()

    images = loadImages()
    drawBoard(screen, colours)

    running = True
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
                
        drawBoard(screen, colours)
        drawPieces(screen, gs.getBoard(), images)
        clock.tick(MAX_FPS)
        pg.display.flip()

    return

if __name__ == "__main__":
    main()
