from machine import Pin, ADC, PWM
from utime import sleep
import _thread
from setup_musique import notes, partitions, NOIRE, CROCHE

ROTARY_ANGLE_SENSOR = ADC(0)
buzzer = PWM(Pin(18))
led = Pin(16,Pin.OUT)
soundVolum = 1
# Variable pour savoir si une note est en cours (évite que le thread réactive le son pendant un silence)
note_en_cours = False 
buttoucount = 1



def btninterruption(pin):
    global buttoucount

    buttoucount += 1

    if buttoucount == 5:
        buttoucount = 1

boutton = Pin(20, Pin.IN, Pin.PULL_UP)
boutton.irq(trigger=Pin.IRQ_FALLING, handler=btninterruption)

def setVolumeButton():
    global soundVolum  
    while True:        
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
        sleep(0.1)     

def changeVolum():
    # On n'applique le volume que si une note doit chanter (évite les bruits pendant les silences)
    if note_en_cours:
        buzzer.duty_u16(soundVolum)
    else:
        buzzer.duty_u16(0)

def playNote(note):
    buzzer.freq(note)

def musicChoice(cptButton): 
    if cptButton == 1 : 
        playPartition("blinding_lights")
        print("play blinding_lights")
    if cptButton == 2 :
        playPartition("get_lucky")
        print("play get_lucky")
    if cptButton == 3 :
        playPartition("star_wars_dark")
        print("play star_wars_dark")   
    if cptButton == 4 :
        playPartition("bad_guy")
        print("play bad_guy")
    

def playPartition(nom_partition):
    global note_en_cours
    
    morceau = partitions[nom_partition]
    
    for note_nom, duree in morceau:
        frequence = notes.get(note_nom, 0)
        
        if frequence > 0:

            playNote(frequence)
            led.value(1)
            note_en_cours = True
            changeVolum()      
        else:
            note_en_cours = False
            buzzer.duty_u16(0)  
            
        sleep(duree)          
        
        # Courte coupure pour détacher les notes identiques qui se suivent
        note_en_cours = False
        led.value(0)
        buzzer.duty_u16(0)
        sleep(0.05)

# Lancement du thread pour le bouton de volume
_thread.start_new_thread(setVolumeButton, ())


while True:
    musicChoice(buttoucount)
    sleep(2)  # Pause de 2 secondes entre chaque répétition du morceau
