import machine
import time
import _thread

led = machine.Pin(18, machine.Pin.OUT)
button = machine.Pin(16, machine.Pin.IN)
#période de chaque pour chaque cycle soit 1 seconde pour 0.5hz soit soit plus vite pour le second cycle 
timeLed1 = 1
timeLed2 = 0.5
#nombre de cliques nécessaires pour obtenir le mode de fonctionnement voulu
buttonStep1 = 1
buttonStep2 = 2
buttonValue = 0
#bolen pour activer ou déactiver le bouton effect à  chaque clique 
buttonEffectActive = False

#fonction lisant l'état du bouton 
def readButton():
    global buttonValue
    global buttonEffectActive

    while True:
        if button.value() == 1:

            # Compte le bouton
            buttonValue = buttonValue + 1

            if buttonValue == 3:
                buttonValue = 0

            # Lance l'effet de 2 secondes
            if buttonEffectActive == False:
                buttonEffectActive = True

            # Attend que le bouton soit relâché
            while button.value() == 1:
                time.sleep(0.01)

            # Anti-rebond
            time.sleep(0.10)

# fonction effectuant le cycle de la led en fonction du compteur de clique 
def ledPower():
    if buttonValue == buttonStep1:
        led.value(1)
        time.sleep(timeLed1)
        led.value(0)
        time.sleep(timeLed1)

    elif buttonValue == buttonStep2:
        led.value(1)
        time.sleep(timeLed2)
        led.value(0)
        time.sleep(timeLed2)

    else:
        led.value(0)


def buttonEffect():
    global buttonEffectActive

    # Allume la LED pendant 2 secondes pour l'effet à chaque appuis 
    led.value(1)
    time.sleep(2)
    led.value(0)
    buttonEffectActive = False


#lancement d'un thread pour lire en continu sur le bouton 
_thread.start_new_thread(readButton, ())


# boucle principale 
while True:

    if buttonEffectActive:
        buttonEffect()

    else:
        ledPower()
