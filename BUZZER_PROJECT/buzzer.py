from machine import Pin, ADC, PWM
from utime import sleep
import _thread
from setup_musique import notes, partitions, NOIRE, CROCHE

ROTARY_ANGLE_SENSOR = ADC(0)
buzzer = PWM(Pin(18))
soundVolum = 1
# Variable pour savoir si une note est en cours (évite que le thread réactive le son pendant un silence)
note_en_cours = False 

def setVolumeButton():
    global soundVolum  # Permet de modifier la variable globale depuis ce thread
    while True:        # Boucle infinie pour lire le bouton en continu
        buttonValue = ROTARY_ANGLE_SENSOR.read_u16()
        
        if buttonValue < 10000: 
            soundVolum = 200
        elif buttonValue < 20000: 
            soundVolum = 400
        elif buttonValue < 30000: 
            soundVolum = 400
        elif buttonValue < 40000: 
            soundVolum = 600
        elif buttonValue < 50000: 
            soundVolum = 800
        else: 
            soundVolum = 800
            
        changeVolum()
        sleep(0.1)     # Petite pause pour ne pas surcharger le processeur (10 lectures par seconde)

def changeVolum():
    # On n'applique le volume que si une note doit chanter (évite les bruits pendant les silences)
    if note_en_cours:
        buzzer.duty_u16(soundVolum)
    else:
        buzzer.duty_u16(0)

def playNote(note):
    buzzer.freq(note)

def playPartition(nom_partition):
    global note_en_cours
    
    # On récupère la liste des tuples (note, durée) depuis setup_musique
    morceau = partitions[nom_partition]
    
    for note_nom, duree in morceau:
        frequence = notes.get(note_nom, 0)
        
        if frequence > 0:
            playNote(frequence)
            note_en_cours = True
            changeVolum()       # Applique le volume actuel
        else:
            note_en_cours = False
            buzzer.duty_u16(0)  # Silence (Pause)
            
        sleep(duree)            # Attend la durée du rythme
        
        # Courte coupure pour détacher les notes identiques qui se suivent
        note_en_cours = False
        buzzer.duty_u16(0)
        sleep(0.02)

# Lancement du thread pour le bouton de volume
_thread.start_new_thread(setVolumeButton, ())

# Boucle principale (le thread principal gère la musique)
while True:
    print("Lecture de Blinding Lights...")
    playPartition("blinding_lights")
    sleep(2)  # Pause de 2 secondes entre chaque répétition du morceau
