import _thread
from lcd1602 import LCD1602
from machine import Pin, ADC, PWM, I2C
from utime import sleep
import time
from dht20 import DHT20

ROTARY_ANGLE_SENSOR = ADC(0)
i2c_lcd = I2C(1, scl=Pin(7), sda=Pin(6), freq=400000)
lcd = LCD1602(i2c_lcd, 2, 16)
i2c_dht20 = I2C(0, sda=Pin(8), scl=Pin(9))
capteur_temp = DHT20(i2c_dht20)

led_pwm = PWM(Pin(16))
led_pwm.freq(1000)
buzzer = PWM(Pin(18))
buzzer.freq(500)
luminosite_pwm = 0
direction_pwm = 1

lcd.clear()
consigne = 20.0

def lcdTemp(tempA, tempC):
    lcd.setCursor(0, 0)
    lcd.print(f"set {tempC}       ")
    lcd.setCursor(0, 1)
    lcd.print(f"Ambient {tempA:.2f}   ")

def lcdAlarm(tempA, tempC):
    temps_ms = time.ticks_ms()
    largeur_ecran = 16
    position = (temps_ms // 150) % largeur_ecran
    
    if (temps_ms // 300) % 2 == 0:
        ligne_texte = [" "] * largeur_ecran
        mot = "ALARM"
        for i in range(len(mot)):
            index = (position + i) % largeur_ecran
            ligne_texte[index] = mot[i]
        texte_final = "".join(ligne_texte)
    else:
        texte_final = " " * largeur_ecran
        
    lcd.setCursor(0, 0)
    lcd.print(texte_final)
    lcd.setCursor(0, 1)
    lcd.print(f"{tempA:.2f}C set {tempC:.2f}C")

def readTemp(): 
    return capteur_temp.dht20_temperature()

def readConsigneLoop():
    global consigne
    tempMin = 15.0
    tempMax = 35.0
    while True:
        buttonValue = ROTARY_ANGLE_SENSOR.read_u16()
        temperature_consigne = tempMin + (buttonValue / 65535.0) * (tempMax - tempMin)
        consigne = round(temperature_consigne, 1)
        sleep(0.1)

def ledcontroller(state): 
    temps_ms = time.ticks_ms()
    if state == 2: 
        if (temps_ms // 100) % 2 == 0:
            led_pwm.duty_u16(30000)
        else:
            led_pwm.duty_u16(0)
    elif state == 1: 
        import math
        intensite = (math.sin((2 * math.pi) * (temps_ms / 2000.0)) + 1.0) / 2.0
        led_pwm.duty_u16(int(intensite * 30000))
    else:
        led_pwm.duty_u16(0)

def buzzerController(state):
    if state == 1:
        buzzer.duty_u16(30000)
    else: 
        buzzer.duty_u16(0)

def thermostatController(temp):
    if temp >= (consigne + 3.0):
        ledcontroller(2)
        buzzerController(1)
        lcdAlarm(temp, consigne)
    elif temp > consigne:
        ledcontroller(1)
        buzzerController(0)
        lcdTemp(temp, consigne)
    else:
        ledcontroller(0)
        buzzerController(0)
        lcdTemp(temp, consigne)

_thread.start_new_thread(readConsigneLoop, ())

while True:
    currentTemp = readTemp()
    thermostatController(currentTemp)
    sleep(0.02)