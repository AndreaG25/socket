import re 
from socket import gethostbyname, gethostname

#Funziona che controlla se l'ip fornito è valido
def valid_IP_Address(sample_str):
    result = True
    match_obj = re.search( r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", sample_str)
    if  match_obj is None:
        result = False
    else:
        for value in match_obj.groups():
            if int(value) > 255:
                result = False
                break
    return result

#Ritorna True se l'ip è corretto, False se l'ip è errato
def test_ip(ip_str):
    if valid_IP_Address(ip_str):
        return True
    else:
        return False
    


#Main -> Funziona che scrive un ip corretto sul file (non è detto sia valido)
while True:
    ip_str = str(input('Inserisci l\'indirizzo IP e la porta del server (IP:PORTA)\n(Invio se il server è situato su questo dispositivo)\n>'))
    if ip_str == '':
        ip = gethostbyname(gethostname())
        port = str(input('Inserisci la porta\n>'))
        while int(port) < 1024 or int(port) > 65535:
            port = str(input('Inserisci la porta\n>'))
        ip_str = f'{ip}:{port}'

    if len(ip_str.split(':')) != 2:
        print('Formato non ammesso, riprova (ip:port)')
    else:
        ip, port = ip_str.split(':')
        if not test_ip(ip) or int(port) < 1024 or int(port) > 65535:
            print('Errore, riprova')
        else:
            myfile = open('ip.txt', 'w')
            myfile.write(ip_str)
            myfile.close()
            print(f'Indirizzo finale: {ip_str}')
            break

