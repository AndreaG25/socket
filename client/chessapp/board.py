import pygame
from chessapp.k import *
from chessapp.general_functions import getJustBoard, getBlackFEN, getCoordinatesFromCubNumber, getPiececWithSquare, getColandRowFromUCI
from chessapp.chess_functions import isThereSomething
import chess
import os

#Caricamento immagini
photo_dir = os.getcwd() + '\\chessapp\\img\\'
b_bishop = pygame.image.load(photo_dir + 'bB.png')
b_king = pygame.image.load(photo_dir + 'bK.png')
b_knight = pygame.image.load(photo_dir + 'bN.png')
b_pawn = pygame.image.load(photo_dir + 'bP.png')
b_queen = pygame.image.load(photo_dir + 'bQ.png')
b_rook = pygame.image.load(photo_dir + 'bR.png')

w_bishop = pygame.image.load(photo_dir + 'wB.png')
w_king = pygame.image.load(photo_dir + 'wK.png')
w_knight = pygame.image.load(photo_dir + 'wN.png')
w_pawn = pygame.image.load(photo_dir + 'wP.png')
w_queen = pygame.image.load(photo_dir + 'wQ.png')
w_rook = pygame.image.load(photo_dir + 'wR.png')


button_arrenditi = pygame.image.load(photo_dir + 'button_arrenditi.png')
button_esc = pygame.image.load(photo_dir + 'button_menu.png')

def drawBoard(WIN):

    #Questo primo if serve per capire il senso della scacchiera, che è relativo al lato del giocare (W/B)
    firstColor = GREEN
    secondColor = WHITE
    
    
    #Riempio la scacchiera di un colore 
    WIN.fill(firstColor)
    WIN.fill(LIGHT_BLACK, rect=(800, 0, WIDTH, HEIGHT))
    #Disegno i quadrati del secondo colore
    for row in range(ROWS):
        for col in range(row % 2, ROWS, 2):
            pygame.draw.rect(WIN, secondColor, (row* SQUARE_SIZE,col* SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    WIN.blit(button_arrenditi, (887, 600))
    WIN.blit(button_esc, (887, 680))


def drawEvents(WIN, color, boardFEN, pieceSelected, legalMoves):
    x, y = getColandRowFromUCI(pieceSelected, color)
    pygame.draw.rect(WIN, YELLOW, (x* SQUARE_SIZE, y* SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    #print(legalMoves)
    for el in legalMoves:      
        if len(el) == 3:
            el = el[:2]
        square = getColandRowFromUCI(el, color)
        #print(f'{square}')
        #print(square)
        x_ = (int(square[0]) * SQUARE_SIZE) + (SQUARE_SIZE/2)
        y_ = (int(square[1]) * SQUARE_SIZE) + (SQUARE_SIZE/2)
        if isThereSomething(boardFEN, el):
            pygame.draw.circle(WIN, GREY, [x_, y_], 50, 7)
        else:
            pygame.draw.circle(WIN, YELLOW, [x_, y_], 12, 0)





def drawPieces(WIN, boardFEN, color):

    #Ottieni dalla fen la prima parte, ovvero la situazione sulla board
    #fen = getJustBoard(boardFEN.fen())

    #Se il lato è nero la stringa viene reversata
    if not color:
        boardFEN = getBlackFEN(boardFEN)
    
    #In ogni caso a me interessa solo la stringa che riguarda i pezzi
    boardFEN = getJustBoard(boardFEN)
    
    #Funzione che dispone i pezzi
    boardList = getPiececWithSquare(boardFEN)
    for el in boardList:
        piece = el[0]
        x, y = getCoordinatesFromCubNumber(el[1])
        if piece == 'r':
            WIN.blit(b_rook, (x* SQUARE_SIZE, y* SQUARE_SIZE))
        elif piece == 'R':
            WIN.blit(w_rook, (x* SQUARE_SIZE, y* SQUARE_SIZE))
        elif piece == 'n':
            WIN.blit(b_knight, (x* SQUARE_SIZE, y* SQUARE_SIZE))
        elif piece == 'N':
            WIN.blit(w_knight, (x* SQUARE_SIZE, y* SQUARE_SIZE))
        elif piece == 'b':
            WIN.blit(b_bishop, (x* SQUARE_SIZE, y* SQUARE_SIZE))
        elif piece == 'B':
            WIN.blit(w_bishop, (x* SQUARE_SIZE, y* SQUARE_SIZE))
        elif piece == 'q':
            WIN.blit(b_queen, (x* SQUARE_SIZE, y* SQUARE_SIZE))
        elif piece == 'Q':
            WIN.blit(w_queen, (x* SQUARE_SIZE, y* SQUARE_SIZE))
        elif piece == 'k':
            WIN.blit(b_king, (x* SQUARE_SIZE, y* SQUARE_SIZE))
        elif piece == 'K':
            WIN.blit(w_king, (x* SQUARE_SIZE, y* SQUARE_SIZE))
        elif piece == 'p':
            WIN.blit(b_pawn, (x* SQUARE_SIZE, y* SQUARE_SIZE))
        elif piece == 'P':
            WIN.blit(w_pawn, (x* SQUARE_SIZE, y* SQUARE_SIZE))
        

def drawMsg(WIN, msg):
    pygame.font.init()
    fontMain = pygame.font.Font('freesansbold.ttf', 50)
    font = pygame.font.Font('freesansbold.ttf', 32)
    textMain = fontMain.render('GAME OVER', True, YELLOW)
    textRectMain = (810, 50)
    WIN.blit(textMain, textRectMain)
    text = font.render(msg, True, WHITE)
    textRect = (810, 120)
    WIN.blit(text, textRect)




class Board:
    msg = ''
    #Costruttore -> Gli passo il colore del giocatore, dal quale poi costrirà la board
    def __init__(self, color):
        self.color = color

    def drawChessBoard(self, WIN, boardFEN, isPieceSelected, pieceSelected, legalMoves):
        #Disegno la scacchiera, ovvero i quadranti
        drawBoard(WIN)
        #Funzione con l'obiettivo di colorare i quadranti nel caso di un pezzo selezionato
        if isPieceSelected:
            drawEvents(WIN, self.color, boardFEN, pieceSelected, legalMoves)
        #Funzione che dalla board inserisce i pezzi
        drawPieces(WIN, boardFEN.fen(), self.color)
        if self.msg != '':
            drawMsg(WIN, self.msg)




    
        
