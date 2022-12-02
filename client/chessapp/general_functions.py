numbers = [1, 2, 3, 4, 5, 6, 7, 8]
letters = ['a','b','c','d','e','f','g','h']

#Funzione che restituisce il quadrante uci dalle coordinate mouse
def getSquareUciFromCoordinate(x, y, color):
    x = getColRowFromCoordinate(x)
    y = getColRowFromCoordinate(y)

    if color:
        return f'{letters[x]}{8-y}'
    else:
        return f'{letters[7-x]}{y+1}'

#funzione che dalle coordinate mouse torna la riga e la colonna (Assoluta)
def getColRowFromCoordinate(num):
    for i in range(8):
        if num >= i*100 and num <= (i*100)+99:
            return i

#Funzione che da una stringa completa FEN ritorna la prima parte ovvero la situazione della scacchiera
def getJustBoard(boardFEN):
    return boardFEN.split(' ')[0]

#Funzione che da una stringa FEN la reversa 
def getBlackFEN(boardFEN):
    boardFEN = boardFEN.split(' ')
    boardFEN[0] = boardFEN[0][::-1]
    boardFEN = ' '.join(boardFEN) 
    return boardFEN


#Funzione che ritorna una lista di liste, al primo posto c'è il pezzo al secondo il numero del quadrane
def getPiececWithSquare(boardFEN):
    c = 63 #Counter del quadrato
    retList = [] #Lista da tornare
    for el in boardFEN:
        if el.isnumeric():
            c -= int(el)
        elif el.isalpha():
            a = []
            a.append(el)
            a.append(c)
            retList.append(a)
            c -= 1
    return retList

#Funzione che dal numero di quadrato ritorna una list con x e y (col e row)
def getCoordinatesFromCubNumber(cubNumber):
    retList = [] #Lista da tornare
    retList.append(7 - (cubNumber%8))
    retList.append(7 - (cubNumber//8))
    return retList

#Funzione che dal quadrante UCI ritorna un la colonna e la rifa
def getColandRowFromUCI(UCISquare, color):
    UCISquare = [*UCISquare]
    retList = []
    if color:
        retList.append(letters.index(UCISquare[0])) #Trova la Col
        retList.append(8-int(UCISquare[1])) #Trova la riga
    else:
        retList.append(7 - letters.index(UCISquare[0]))
        retList.append(int(UCISquare[1])-1)
    return retList

