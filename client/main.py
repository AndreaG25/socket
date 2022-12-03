import socket
import threading
import pygame
import chess
import webbrowser
from os import getcwd, system
from chessapp.button import Button
from chessapp.k import WIDTH, HEIGHT
from chessapp.board import Board
from chessapp.general_functions import getSquareUciFromCoordinate
from chessapp.chess_functions import isThereSomething, whichColor, getCodeMoveFromPosition
















#General variables shared
FORMAT = 'utf-8'
PLAY_MESSAGE = '!PLAY'




#Creating socket tcp client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Funzione che va a leggere il file ip.txt, se trova in ip lo restituisce, altrimento lo fa impostare
def getAddressFromFile():
    myfile = open('ip.txt', 'r')
    addr = myfile.readline()
    myfile.close()
    if addr == '':
        print(f'Il file è vuoto, ora te lo faccio impostare')
        system('python setAdd.py')
    else:
        ip, port = addr.split(':')
        address = (ip, int(port))
        print(f'address: {address}')
    
    if addr == '':
        address = getAddressFromFile()
    return address
    

#Questo ciclo tenta di creare la connessione finchè non viene inserito/trovato l'ip giusto
while True:
    try:
        address = getAddressFromFile()
        print(f'Mi provo a connettere a {address}')
        client.connect(address)
    except:
        print('Indirizzo non valido, impostare uno nuovo')
        system('python setAdd.py')
    else:
        print(f'Mi sono connesso a {address}')
        break
        

#Crea la schermata di gioco
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('AGCHESS')


#Variabili globali per il corretto funzionamento del gioco


#Color -> indica il lato del giovare (True -> White, False -> Black) (Mandato dal Server)
color = True

#codeMove -> il numero che il client manda al server per il codice mossa (Vedi protocollo)
codeMove = ''

#codeMatch -> Codice identificatico della partita (Mandato dal Server)
codeMatch = ''

#termined -> Appena la partita finisce diventa False (Per evitare che si possano toccare ancora i pezzi)
global termined 
termined = False

#pieceToPromove -> Indica il pezzo che viene scambiato una volta che il pedone raggiunge il fondo della scacchiera
#Di base è q (Regina) e non viene mai modificato
pieceToPromove = 'q'

#Quando è True pygame mostrerà l'interfaccia menu, quando è false la partita 
global menu
menu = True




#load button images
wallpaper_img = pygame.image.load(getcwd() + '\\assets\wallpaper.jpg')
agchess_img = pygame.image.load(getcwd() + '\\assets\\title2.png')
quit_img = pygame.image.load(getcwd() + '\\assets\quit.png')
play_img = pygame.image.load(getcwd() + '\\assets\\button_play.png')
about_img = pygame.image.load(getcwd() + '\\assets\\button_about.png')

#create button instances
play_button = Button(350, 300, play_img)
about_button = Button(350, 400, about_img)
exit_button = Button(350, 500, quit_img)

#Funzione che server per gestire i messaggi che arrivano dal server
#Praticamente questa funziona crea e gestisce la partita lato client

def listenServer():
    global termined
    while True:
        msg = wait4message()
        msgSplitted = msg.split(':')
        if len(msgSplitted) == 1:
            code = msgSplitted[0]
        elif len(msgSplitted) == 3:
            code = msgSplitted[1]
            move = msgSplitted[2]
        else:
            input('Qualcosa è andato storto...\n')

            
        if code == '201':
            print('Vai bianco')
        elif code == '202':
            print('La mossa eseguita dal bianco: ' + str(move))
            logicalBoard.push_uci(move)
        elif code == '203':
            print('La mossa eseguita dal nero: ' + str(move))
            logicalBoard.push_uci(move)
        elif code == '205':
            graphicBoard.msg = f'Hai perso'
            logicalBoard.push_uci(move)
            termined = True
        elif code == '207':
            graphicBoard.msg = f'Ripetizione di mosse'
            logicalBoard.push_uci(move)
            termined = True
        elif code == '208':
            graphicBoard.msg = f'Materiale insufficiente'
            logicalBoard.push_uci(move)
            termined = True
        elif code == '209':
            graphicBoard.msg = f'Stallo'
            logicalBoard.push_uci(move)
            termined = True
        elif code == '210':         
            graphicBoard.msg = f'Vinto per abbandono'
            termined = True


#richiama con un thread la listenServer, per avere istruzioni dal server
#setta la variabile menu falsa (per mostrare la scacchiera)
#crea la scacchiera logica (logicalBoard)
#crea la scacchiera grafica (graphicBoard)
def startMatch():
    threading.Thread(target=listenServer, args=[]).start()
    global menu 
    menu = False
    #locicalBoard -> La board logica create con il modulo python-chess, le funzionalitò del gioco passano da qua
    #Questa rimane invariata sia per bianco per nero
    global logicalBoard
    logicalBoard = chess.Board()
    #'rnbqk1nr/ppp1b1Pp/3p4/4p3/8/8/PPPP1PPP/RNBQKBNR w KQkq - 1 5' per promozione
    #locicalBoard.push_san('e4')
    #locicalBoard.push_san('Nc6')
    #graphicBoard -> Questo oggetto importato dal file board.py è l'interfaccia grafica
    #Viene inizialiazzata con il colore del giocatore (True = White, False = Black)
    global graphicBoard
    graphicBoard = Board(color)
    graphicBoard.drawChessBoard(WIN, logicalBoard, False, '', [])
    pygame.display.update()

    
    
    
        
        

#Il server sta aspettando un avversario che voglia giocare, una volta che arriva (cod. 3) inizia la partita 
def wait4secondPlayer():
    print('WAITING FOR A SECOND PLAYER')
    res = wait4message()
    resSplitted = res.split(':')
    if resSplitted[0] == '3':
        global color
        global codeMove
        global codeMatch
        color = True
        codeMove = '202'
        codeMatch = resSplitted[1]
        startMatch()
    else:
        print('Error')

#Funzione che aspetta un messaggio e quando lo riceve lo ritorna
def wait4message():
    while True:
        msg = client.recv(1024).decode(FORMAT)
        return msg



#Funzione che manda al server !PLAY il comando per giocare
def sendPlayMsg():
    sendMessage(PLAY_MESSAGE)
    res = wait4message()
    resSplitted = res.split(':')
    if resSplitted[0] == '1':
        #print('Sono il bianco')
        wait4secondPlayer()
    elif resSplitted[0] == '2':
        #print('Sono il nero')
        global color
        global codeMove
        global codeMatch
        color = False
        codeMove = '203'
        codeMatch = resSplitted[1]
        startMatch()


#Funzione standard che manda un messaggio
def sendMessage(msg):
    client.send(bytes(f'{msg}$',FORMAT))



#game loop
run = True

#Variabile booleana che verifica se un pezzo è selezionato
isPieceSelected = False

#Variabile stringa con il quadrante selezionato in formato UCI
squareSelected = ''

#List che contiene le mosse legali
moves = []


#Gestione della UI
while run:
    if menu:
        WIN.blit(wallpaper_img, (0, 0))
        WIN.blit(agchess_img, (158, 0))
        if play_button.press(WIN):
            threading.Thread(target=sendPlayMsg, args=[]).start()
        elif about_button.press(WIN):
            webbrowser.open('https://github.com/AndreaG25/socket')
        elif exit_button.press(WIN):
            run = False
    else:
        graphicBoard.drawChessBoard(WIN, logicalBoard, isPieceSelected, squareSelected, moves)
    pygame.display.update()

	#event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONUP and not menu:
            x, y = pygame.mouse.get_pos()
            #nel caso la x non sia nella scacchiera devo verificare se sono stati premuti i bottoni
            if x < 800:
                squareUCI = getSquareUciFromCoordinate(x, y, color) #Ottengo il quadrante dalle coordinate
                
                #Sezione che muovere i pezzi
                if isPieceSelected and whichColor(logicalBoard, squareUCI) != color and (not termined):
                    for el in moves:
                        if len(el) == 3 and el[:2] == squareUCI:
                            logicalBoard.push_uci(f'{squareSelected}{el[:2]}{pieceToPromove}')
                            newCodeMove = getCodeMoveFromPosition(logicalBoard, codeMove)
                            if newCodeMove == '205':
                                graphicBoard.msg = f'Hai vinto'
                            elif newCodeMove == '207':
                                graphicBoard.msg = f'Ripetizione di mosse'
                            elif newCodeMove == '208':
                                graphicBoard.msg = f'Materiale insufficiente'
                            elif newCodeMove == '209':
                                graphicBoard.msg = f'Stallo'
                            if newCodeMove != codeMove:
                                termined = True
                            sendMessage(f'{codeMatch}:{newCodeMove}:{squareSelected}{el[:2]}{pieceToPromove}')
                            break #break perche ci entrerebbe + volte

                        elif len(el) == 2 and el == squareUCI:
                            logicalBoard.push_uci(f'{squareSelected}{el}')    
                            newCodeMove = getCodeMoveFromPosition(logicalBoard, codeMove)
                            if newCodeMove == '205':
                                graphicBoard.msg = f'Hai vinto'
                                termined = True
                            elif newCodeMove == '207':
                                graphicBoard.msg = f'Ripetizione di mosse'
                                termined = True
                            elif newCodeMove == '208':
                                graphicBoard.msg = f'Materiale insufficiente'
                                termined = True
                            elif newCodeMove == '209':
                                graphicBoard.msg = f'Stallo'
                                termined = True
                            if newCodeMove != codeMove:
                                termined = True
                            #print(f'{codeMatch}:{newCodeMove}:{squareSelected}{el}')
                            sendMessage(f'{codeMatch}:{newCodeMove}:{squareSelected}{el}')
                        
                            

                   
                #In caso seleziona un quadrante con un mio pezzo devo trovare le mosse legali
                if isThereSomething(logicalBoard, squareUCI) and whichColor(logicalBoard, squareUCI) == color and (not termined):
                    squareSelected = squareUCI
                    isPieceSelected = True
                    moves = []
                    for el in logicalBoard.legal_moves:
                        if str(el)[:2] == squareSelected and len(str(el)) > 4:
                            moves.append(str(el)[-3:])
                        elif str(el)[:2] == squareSelected:
                            moves.append(str(el)[-2:])
                else:
                    isPieceSelected = False
                    #Ha premuto un quadrante vuoto
                
            else:
                #controllo se ha premuto il tasto 'arrenditi'
                if x >= 887 and x <= 1115 and y >= 600 and y <= 666 and color == logicalBoard.turn:
                    if not termined:
                        graphicBoard.msg = f'Hai abbandonato'
                        sendMessage(f'{codeMatch}:210:{color}')
                        termined = True
                #controllo se ha premuto il tasto torna al 'menu principale'
                elif x >= 887 and x <= 1115 and y >= 680 and y <= 746 and termined:
                    pygame.quit()
                    system('python main.py')
                    
                        
            
    

pygame.quit()











