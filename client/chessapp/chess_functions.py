import chess

#Funzione che controlla se è presente qualcosa in un determinato quadrante, tramite un UCI
def isThereSomething(boardFEN, squareUCI):
    #print(f'Il quadrante {squareUCI} corrisponde al numero {chess.parse_square(squareUCI)}')
    #print(f'{type(boardFEN)} {chess.parse_square(squareUCI)}')
    #print(f'{type(boardFEN.piece_at(chess.parse_square(squareUCI)))}')
    if type(boardFEN.piece_at(chess.parse_square(squareUCI))) != type(None):
        return True
    else:
        return False

#Funzione che dato un quadrante ritorna il colore 
def whichColor(boardFEN, squareUCI):
    #print(boardFEN.color_at(chess.parse_square(squareUCI)))
    return boardFEN.color_at(chess.parse_square(squareUCI))

#Funzione che gestisce i finali, da una situazione ritorna il codice corrispondente (es. rileva scacco matto, ritorna 205)
def getCodeMoveFromPosition(boardFEN, currentCode):
    #newBoard = chess.Board(boardFEN)
    if boardFEN.is_game_over():
        if boardFEN.is_checkmate():
            return '205'
        elif boardFEN.is_fivefold_repetition():
            return '207'
        elif boardFEN.is_insufficient_material():
            return '208'
        elif boardFEN.is_stalemate():
            return '209'
    else:
        return currentCode
