from Carta import Carta
from CartaInMano import CartaInMano
from CartaInCampo import CartaInCampo
from Mana import Mana
from CartaDaGiocareInDifesa import CartaDaGiocareInDifesa
from Attacco import Attacco
import cv2
import pyautogui
import numpy as np
import subprocess
import time
import colorama
from colorama import init, Fore, Back, Style
import os
import re
from platforms.desktop.desktop_handler import DesktopHandler
from specializations.dlv2.desktop.dlv2_desktop_service import DLV2DesktopService
from languages.asp.asp_mapper import ASPMapper
from languages.asp.asp_input_program import ASPInputProgram
from lib.EmbASP.base.option_descriptor import OptionDescriptor
from lib.EmbASP.languages.asp.symbolic_constant import SymbolicConstant

os.system('color')
colorama.init()

# Avvio programma per effettuare screen mirroring
subprocess.Popen('Smartphone Mirror/scrcpy.exe')
# Intervallo per avviare programma in sicurezza
time.sleep(2) 

# Acquisizione informazioni sulla finestra aperta
window = pyautogui.getActiveWindow()

# Stampa dimensione finestra
print(f'Larghezza: {window.width} Altezza: {window.height}')

# Coordinate posizione mirror del telefono
x = 0
y = 0

# Spostamento finestra in coordinate (x, y)
window.moveTo(x, y)

# -------------------------------------------------------------------------------------------------------
#                       Dichiarazione template necessari per riconoscimento immagini
# -------------------------------------------------------------------------------------------------------

# TemplateCarteInMano carte da riconoscere in mano
templatesCarteInMano = [cv2.imread("img/character/knight.png"), cv2.imread("img/character/minion.png"), cv2.imread("img/character/archers.png"), cv2.imread("img/character/giant.png"), cv2.imread("img/character/pekka.png"), cv2.imread("img/character/musketeer.png"), cv2.imread("img/character/arrows.png"), cv2.imread("img/character/fireball.png")]

# TemplateCarteInCampo per unità da riconoscere in campo
templatesCarteInCampo = [cv2.imread("img/character/knightInCamp.png"), cv2.imread("img/character/knightInCamp1.png"), cv2.imread("img/character/minionInCamp.png"), cv2.imread("img/character/minionInCamp1.png"), cv2.imread("img/character/archersInCamp.png"), cv2.imread("img/character/archersInCamp1.png"), cv2.imread("img/character/giantInCamp.png"), cv2.imread("img/character/giantInCamp1.png"), cv2.imread("img/character/giantInCamp2.png"), cv2.imread("img/character/pekkaInCamp.png"), cv2.imread("img/character/pekkaInCamp1.png"), cv2.imread("img/character/pekkaInCamp2.png"), cv2.imread("img/character/musketeerInCamp.png"), cv2.imread("img/character/musketeerInCamp1.png"), cv2.imread("img/character/livello.png")]

# TemplateManaDisponibile immagini per riconoscimento del mana disponibile
templatesManaDisponibile = [cv2.imread("img/mana/0.png"), cv2.imread("img/mana/1.png"), cv2.imread("img/mana/2.png"), cv2.imread("img/mana/3.png"), cv2.imread("img/mana/4.png"), cv2.imread("img/mana/5.png"), cv2.imread("img/mana/6.png"), cv2.imread("img/mana/7.png"), cv2.imread("img/mana/8.png"), cv2.imread("img/mana/9.png"), cv2.imread("img/mana/10.png")]

# Posizione delle carte in mano su screen mirroring
posizioniCarteInMano = [(107, 860), (187, 859), (268, 859), (349, 859)]

# Dimensione rettangoli delle carte in mano per fare match su screen mirroring
dimensioniCarteInMano = [(68, 84), (69, 86), (69, 86), (69, 85)]

# Nome delle carte e quantità di mana disponibile
nomeCarteInMano = ["knight", "minion", "archers", "giant", "pekka", "musketeer", "arrows", "fireball"]
nomeCarteInCampo = ["knight", "knight", "minion", "minion", "archers", "archers", "giant", "giant", "giant", "pekka", "pekka", "pekka", "musketeer", "musketeer", "livello", "arrows", "fireball"]
nomeMana = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Inizializzazione nome della carta avversaria in campo 
nomeCartaInCampoTrovata = ""

# Coordinata X linea immaginaria sulla quale l'IA fa riferimento per posizionare le carte in sicurezza
xWindowSicura = 800

# Coordinata X massima del campo
xWindowMax = 900

# Coordinata X dell'ultima carta giocata
xUltimaCartaGiocata = 0

usedMana = 7

# -------------------------------------------------------------------------------------------------------
#                                   Esecuzione Intelligenza Articiale
# -------------------------------------------------------------------------------------------------------

while True:
    handler = DesktopHandler(DLV2DesktopService("executable/dlv2.exe"))

    ASPMapper.get_instance().register_class(Carta)
    ASPMapper.get_instance().register_class(CartaDaGiocareInDifesa)
    ASPMapper.get_instance().register_class(Attacco)
    ASPMapper.get_instance().register_class(CartaInMano)
    ASPMapper.get_instance().register_class(CartaInCampo)
    ASPMapper.get_instance().register_class(Mana)

    inputProgram = ASPInputProgram()

    option = OptionDescriptor("-n 1")
    handler.add_option(option)

    #Regole per l'attacco
    attackRules = "attacco(Nome) | nAttacco(Nome) :- cartaInMano(Nome)."
    attackRules += ":- attacco(Nome), carta(Nome,Mana,Tipo,Forza,Target), manaDisponibile(ManaDisponibile), ManaDisponibile < Mana."
    attackRules += ":- attacco(Nome), carta(Nome,Mana,Tipo,Forza,Target), Tipo == 2."
    attackRules += ":- #count{Nome : attacco(Nome)} < 1."
    attackRules += ":~ attacco(Nome), carta(Nome,Mana,Tipo,Forza,Target). [Target@1,Nome,Mana,Tipo,Forza,Target]"

    #Regole per la difesa
    defendRules = "cartaDaGiocareInDifesa(Nome) | nCartaDaGiocareInDifesa(Nome) :- cartaInMano(Nome)."
    defendRules += ":- cartaDaGiocareInDifesa(Nome), carta(Nome,Mana,Tipo,Forza,Target), Target == 1."
    defendRules += ":- cartaDaGiocareInDifesa(Nome), carta(Nome,Mana,Tipo,Forza,Target), manaDisponibile(ManaDisponibile), ManaDisponibile < Mana."
    defendRules += ":- cartaDaGiocareInDifesa(Nome), cartaInCampo(Nome1), carta(Nome,Mana,Tipo,Forza,Target), carta(Nome1,Mana1,Tipo1,Forza1,Target1), Target < Target1."
    defendRules += ":- #count{Nome : cartaDaGiocareInDifesa(Nome)} < 1."
    defendRules += ":~ cartaDaGiocareInDifesa(Nome), carta(Nome,Mana,Tipo,Forza,Target). [Tipo@1,Nome,Mana,Tipo,Forza,Target]"
    
    
    inputProgram.add_program("carta(knight, 3, 1, 5, 2).")
    inputProgram.add_program("carta(minion, 3, 1, 2, 4).")
    inputProgram.add_program("carta(archers, 3, 1, 3, 4).")
    inputProgram.add_program("carta(arrows, 3, 2, 3, 4).")
    inputProgram.add_program("carta(fireball, 4, 2, 6, 4).")
    inputProgram.add_program("carta(giant, 5, 1, 8, 1).")
    inputProgram.add_program("carta(pekka, 4, 1, 7, 2).")
    inputProgram.add_program("carta(musketeer, 4, 1, 6, 4).")
    inputProgram.add_program("carta(livello, 11, 1, 4, 4).")
    #inputProgram.add_objects_input(get_carte())
    
    # Acquisizione screen del mirror
    screenshot = pyautogui.screenshot(region=(x, y, window.width, window.height))
    screenshot.save('img/clashroyale.png')

    # Lettura screen del mirror
    letturaScreenshot = cv2.imread('img/clashroyale.png')

    # Inizializzazione carte che si hanno in mano
    carteInMano = [""] * 4

    # Aggiornamento della carta avversaria riconosciuta in campo 
    nomeCartaInCampoTrovata = ""

    # Posizione iniziale della carta in campo riconosciuta
    xCardInCampo = 0
    yCardInCampo = 0

    # Posizione iniziale della carta in campo sconosciuta
    xLivello = 0
    yLivello = 0

    # Posizione aggiornata della carta sconosciuta (livello rosso presente su ogni personaggio avversario schierato)
    cartaNonRiconosciutaInCampo = ""

    # Inizializzazione quantità di mana disponibile
    manaTrovato = 0

    

    #carta(Nome, Costo In Mana, Tipologia (1 = unità, 2 = magia), Livello di Forza, Tipo Target(1 = edifici, 2 = unità di terra, 3 = unità d'aria, 4 = tutte le tipologie))

    # Scorrimento possibili carte in campo
    for i, templateCartaInCampo in enumerate(templatesCarteInCampo):
        # Verifica presenza di Livello in campo e salvataggio informazioni
        if nomeCarteInCampo[i] == "livello":
            matchImmagine = cv2.matchTemplate(letturaScreenshot, templateCartaInCampo, cv2.TM_CCOEFF_NORMED)
            posizioniMatchImmagine = np.where(matchImmagine >= 0.8)

            if len(posizioniMatchImmagine[0]) > 0:
                xLivello = posizioniMatchImmagine[1][0]
                yLivello = posizioniMatchImmagine[0][0]
                cartaNonRiconosciutaInCampo = nomeCarteInCampo[i]

                inputProgram.add_program("cartaInCampo(" + cartaNonRiconosciutaInCampo + ").")
        else:
            # Verifica templateCartaInCampo, quindi presenza in campo di una determinata carta
            matchImmagine = cv2.matchTemplate(letturaScreenshot, templateCartaInCampo, cv2.TM_CCOEFF_NORMED)
            posizioniMatchImmagine = np.where(matchImmagine >= 0.6)

            # Controllo riconoscimento della carta, e determina la carta da giocare
            if len(posizioniMatchImmagine[0]) > 0:
                xCardInCampo = posizioniMatchImmagine[1][0]
                yCardInCampo = posizioniMatchImmagine[0][0]
                nomeCartaInCampoTrovata = nomeCarteInCampo[i]

                # Fatto pyDatalog per carta in campo
                inputProgram.add_program("cartaInCampo(" + nomeCartaInCampoTrovata + ").")

    # Scorrimento possibili carte in mano
    for h, templateCartaInMano in enumerate(templatesCarteInMano):
        # Ricerca carte nelle posizioni delle carte in mano su mirror
        for j, posizioneCartaInMano in enumerate(posizioniCarteInMano):
            dimensioneCartaInMano = dimensioniCarteInMano[j]
            posizioniRicerca = letturaScreenshot[posizioneCartaInMano[1]:posizioneCartaInMano[1]+dimensioneCartaInMano[1], posizioneCartaInMano[0]:posizioneCartaInMano[0]+dimensioneCartaInMano[0]]
            matchImmagine = cv2.matchTemplate(posizioniRicerca, templateCartaInMano, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(matchImmagine)
            if max_val > 0.8:
                nomeCarta = nomeCarteInMano[h]
                carteInMano[j] = nomeCarta
    
    # Inserimento fatti pyDatalog per carte in mano 
    for k, cartaInManoSelezionata in enumerate(carteInMano):
        inputProgram.add_program("cartaInMano(" + cartaInManoSelezionata + ").")
        print(f"Hai {cartaInManoSelezionata} in {k} posizione")
    
    # Verifica disponibilità di mana
    for l, mana in enumerate(templatesManaDisponibile):
        matchImmagine = cv2.matchTemplate(letturaScreenshot, mana, cv2.TM_CCOEFF_NORMED)
        posizioniMatchImmagine = np.where(matchImmagine >= 0.98)
        if len(posizioniMatchImmagine[0]) > 0:
            manaTrovato = nomeMana[l]
            print(f"{Fore.BLUE}Hai {manaTrovato} disponibile{Fore.RESET}")

    # Fatto pyDatalog per disponibilità mana
    inputProgram.add_program(f"manaDisponibile({manaTrovato}).")
    
    handler.add_program(inputProgram)

    if nomeCartaInCampoTrovata != "":
        inputProgram.add_program(defendRules) 
        answerSets = handler.start_sync()
        
        print(f"{Fore.RED}La carta in campo e': {nomeCartaInCampoTrovata}{Fore.RESET}")
        if(len(answerSets.get_optimal_answer_sets()) > 0):
            answerSet = answerSets.get_optimal_answer_sets()[0]
            if 'cartaDaGiocareInDifesa' in str(answerSet):
                risultatoRegex = re.search('cartaDaGiocareInDifesa\((.*?)\)', str(answerSet))
                for j, cartaInManoSelezionata in enumerate(carteInMano):
                    if cartaInManoSelezionata == risultatoRegex.group(1):
                        
                        # Movimento cursore al centro della carta da giocare
                        pyautogui.moveTo(posizioniCarteInMano[j][0] + 30, posizioniCarteInMano[j][1] + 35)

                        # Click su schermo
                        pyautogui.click()

                        # Verifica se carta da giocare è una spell, quindi calcola posizione di lancio
                        if cartaInManoSelezionata == "arrows":
                            pyautogui.moveTo(xCardInCampo + 2, yCardInCampo + 95)
                        elif cartaInManoSelezionata == "fireball":
                            pyautogui.moveTo(xCardInCampo + 2, yCardInCampo + 110)
                        else:
                            # Verifica se carta da giocare è un'unità con alto range, quindi calcola posizione di lancio
                            if cartaInManoSelezionata == "archers" or cartaInManoSelezionata == "musketeer" or cartaInManoSelezionata == "minion" :
                                pyautogui.moveTo(xCardInCampo + 2, ((xWindowMax * (((xWindowSicura - yCardInCampo)))/xWindowSicura)/2) + yCardInCampo)
                            else:
                                pyautogui.moveTo(xCardInCampo + 2, ((xWindowMax * (((xWindowSicura - yCardInCampo)))/xWindowSicura)/2.5) + yCardInCampo)
                        
                        # Click su schermo
                        pyautogui.click()

                        # Salvataggio coordinata X della carta giocata 
                        xUltimaCartaGiocata = xCardInCampo
                        nomeCartaInCampoTrovata = ""
    else:
        if cartaNonRiconosciutaInCampo != "":  
            inputProgram.add_program(defendRules) 
            answerSets = handler.start_sync()

            print(f"{Fore.RED}Una carta sconosciuta e' in campo{Fore.RESET}")
            if(len(answerSets.get_optimal_answer_sets()) > 0):
                answerSet = answerSets.get_optimal_answer_sets()[0]
                if 'cartaDaGiocareInDifesa' in str(answerSet):
                    risultatoRegex = re.search('cartaDaGiocareInDifesa\((.*?)\)', str(answerSet))
                    for j, cartaInManoSelezionata in enumerate(carteInMano):
                        if cartaInManoSelezionata == risultatoRegex.group(1):
                            # Spostamento cursore al centro dello schermo
                            pyautogui.moveTo(posizioniCarteInMano[j][0] + 30, posizioniCarteInMano[j][1] + 35)

                            # Click su schermo
                            pyautogui.click()
                            
                            if cartaInManoSelezionata == "arrows":
                                pyautogui.moveTo(xLivello + 2, yLivello + 95)
                            elif cartaInManoSelezionata == "fireball":
                                pyautogui.moveTo(xLivello + 2, yLivello + 110)
                            else:
                                if cartaInManoSelezionata == "archers" or cartaInManoSelezionata == "musketeer" or cartaInManoSelezionata == "minion":
                                    pyautogui.moveTo(xLivello + 2, ((xWindowMax * (((xWindowSicura - yLivello)))/xWindowSicura)/2) + yLivello)
                                else:
                                    pyautogui.moveTo(xLivello + 2, ((xWindowMax * (((xWindowSicura - yLivello)))/xWindowSicura)/2.5) + yLivello)
                                    
                            xUltimaCartaGiocata = xLivello
                            # Click su schermo
                            pyautogui.click()
        else:
            inputProgram.add_program(attackRules) 
            answerSets = handler.start_sync()
            if((len(answerSets.get_optimal_answer_sets()) > 0) and manaTrovato >= usedMana):
                answerSet = answerSets.get_optimal_answer_sets()[0]
                if 'attacco' in str(answerSet):
                    risultatoRegex = re.search('attacco\((.*?)\)', str(answerSet))
                    for f, cartaInManoSelezionata in enumerate(carteInMano):
                        if cartaInManoSelezionata == risultatoRegex.group(1):
                            
                            #Modifica del mana necessario per attaccare
                            if(usedMana == 3):
                                usedMana = 7
                            else:
                                usedMana = 3

                            # Spostamento cursore al centro dello schermo
                            pyautogui.moveTo(posizioniCarteInMano[f][0] + 30, posizioniCarteInMano[f][1] + 35)

                            # Click su schermo
                            pyautogui.click()
                            
                            # La carta in attacco viene posizionata, sulla stessa coordinata X della precedente
                            if xUltimaCartaGiocata != 0:
                                pyautogui.moveTo(xUltimaCartaGiocata, posizioniCarteInMano[f][1] - 250)
                                xUltimaCartaGiocata = xUltimaCartaGiocata
                            else:
                                pyautogui.moveTo(posizioniCarteInMano[f][0], posizioniCarteInMano[f][1] - 250)
                                xUltimaCartaGiocata = posizioniCarteInMano[f][0]
                            
                            # Click su schermo
                            pyautogui.click()