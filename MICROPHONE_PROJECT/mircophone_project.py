from ws2812 import WS2812
import machine
import utime
import random

SEUIL_BATTEMENT = 1500  
TEMPS_VERROU_MS = 180
dernier_battement = utime.ticks_ms()

microphone = machine.ADC(0)
led = WS2812(18, 1)

def readMicrophone(): 
    sound = microphone.read_u16()
    return sound

def generer_couleur_aleatoire():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

# Éteindre la LED au démarrage
led.pixels_fill((0, 0, 0))
led.pixels_show()

while True:
    volume = readMicrophone()
    temps_actuel = utime.ticks_ms()
    
    if volume > SEUIL_BATTEMENT and utime.ticks_diff(temps_actuel, dernier_battement) > TEMPS_VERROU_MS:
        
        couleur_aleatoire = generer_couleur_aleatoire()
        
        led.pixels_fill(couleur_aleatoire)
        led.pixels_show()
        
        # Mise à jour du chronomètre pour le prochain battement
        dernier_battement = temps_actuel
        print("Battement détecté ! Volume :", volume)
        
    utime.sleep_ms(10)