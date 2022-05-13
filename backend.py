from entrada import Entrada
import time
import datetime
import text as tx
#import face_shot as fs
#import train_model as tm
#import face_rec as fr
import os


#Buscar un dorsal x en una llista list, retorna la posicio del dorsal si el troba, altrament retorna -1
def search(list, x):
    for i in range(len(list)):
        if list[i].dorsal == x:
            return i
    return -1

def primeraPosLliure(pendent):
    for i in range(len(pendent)):
        if pendent[i] is None:
            return i
    return -1


def primeraPosCreate(pendent):
    for i in range(len(pendent)):
        if pendent[i] is not None and pendent[i].estat == "create":
            return i
    return -1


def primeraPosStart(pendent):
    for i in range(len(pendent)):
        if pendent[i] is not None and pendent[i].estat == "start":
            return i
    return -1

def main():
    pendent = [None] * 4
    while 1:
        print("1. Afegir entrada")
        print("2. Eliminar entrada")
        print("3. Senyal de start")
        print("4. Senyal de stop")
        print("5. Veure classificacio")
        print("6. Clear Database")
        print("7. Registrar")
        print("8. Exit")
        text = input()
        print()
        if text == "1":     #afegir entrada
            print("Escriu el dorsal del player:")
            text = input()
            if "1" <= text <= "999":
                primeraPos = primeraPosLliure(pendent)
                #print(primeraPos)
                if primeraPos == -1:
                    print("Ja hi ha 4 entrades")
                else:
                    entrada = Entrada(text)
                    pendent[primeraPos] = entrada
                    print("Entrada afegida a la posicio " + str(primeraPos))
            else:
                print("El dorsal ha de ser un numero entre 1 i 999")
        elif text == "2":   #eliminar entrada
            print("Escriu l'entrada que vols eliminar:")
            text = input()
            if "0" <= text <= "3":
                pendent[int(text)] = None
                print("Entrada de la posicio " + text + " eliminada")
            else:
                print("L'entrada ha de ser un numero entre 0 i 3")
        elif text == "3":   #start
            primeraPos = primeraPosCreate(pendent)
            #print(primeraPos)
            if primeraPos != -1:
                pendent[primeraPos].estat = "start"
                pendent[primeraPos].temps = time.time()
                print("Comptador començat en l'entrada " + str(primeraPos))
            else:
                print("No hi ha cap entrada on pugui començar el comptador")
        elif text == "4":   #stop---------------------------------------------------------------------------------
            primeraPos = primeraPosStart(pendent)
            #print(primeraPos)
            if primeraPos != -1:
                pendent[primeraPos].temps = time.time() - pendent[primeraPos].temps

                dorsal= str(pendent[primeraPos].dorsal)
                rnumber= tx.get_run_number(dorsal)
                data= str(datetime.datetime.now())
                temps= str(pendent[primeraPos].temps)
                pista= tx.get_current_pista()
                textinput= dorsal+','+rnumber+','+data+','+temps+','+pista+'\n'
                tx.add_text(textinput)

                print("Comptador aturat en l'entrada " + str(primeraPos))
                pendent[primeraPos] = None
            else:
                print("No hi ha cap entrada on pugui aturar el comptador")
        elif text == "5":
            print("1. Classificacio de tots els runs de tots els players")
            print("2. Classificacio del millor run de tots els players")
            print("3. Classificacio del RUN 1 de tots els players")
            print("4. Classificacio de tots els runs de un player")
            print("5. Back")

            text = input()
            print()
            if text == "1":     #Classificacio de tots els runs de tots els players
                contents= tx.get_all_ranking()
                print(contents)

            elif text == "2":   #Classificacio del millor run de tots els players
                contents= tx.get_best_rank()
                print(contents)

            elif text == "3":   #Classificacio del RUN 1 de tots els players
                contents= tx.get_run_one()
                print(contents)

            elif text == "4":   #Classificacio de tots els runs de un player
                print("Escriu el dorsal del player:")
                dorsal = input()
                contents= tx.get_runs_player(dorsal)
                print(contents)

        elif text == "6":
            return_value= tx.clear_file()
            if (return_value==-1):
                print("Les dades ja eren netes")
        elif text == "7":
            print("Introdueix el teu nom i cognom:")
            nom = input()
            if not os.path.exists("dataset/"+nom):
                os.makedirs("dataset/"+nom)
            fs.face_shot(nom)
            tm.train_model()
            name_cam = fr.face_rec()
            print(name_cam)
        else:
            return
        print()
