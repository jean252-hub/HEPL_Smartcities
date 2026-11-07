### Warning selon le servo moteur choisi l'horlogue peut parfois tourner dans le sens inverse des aiguilles d'une montre !
### pour eviter cela il suffit de faire 180 - angle lorsque l'on utilise la fonction servo.turn

import network
import ntptime
from machine import Pin
from utime import sleep_ms, ticks_ms, ticks_diff, localtime, time
from servo import Servo
from wifi_setup import WIFI_SSID, WIFI_PASSWORD, WIFI_TIMEOUT_MS

BUTTON_PRESSED_LEVEL = 1
button = Pin(16, Pin.IN)

DEBOUNCE_MS = 200
Hours_mode = False #False 12 True 24
servo = Servo(Pin(20))

last_press = ticks_ms()
last_update = ticks_ms()
last_click = 0
double_click = 400

TIMEZONES = [
    ("UTC", 0),
    ("UTC+1", 1),
    ("UTC+2", 2),
    ("UTC+3", 3),
    ("UTC+8", 8),
    ("UTC+9", 9),
    ("UTC-5", -5),
    ("UTC-8", -8),
]
tz_index = 1  # on démarre sur UTC+1 (heure d'hiver de Paris)


def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)

        start = ticks_ms()

        while not wlan.isconnected():
            if ticks_diff(ticks_ms(), start) >= WIFI_TIMEOUT_MS:
                raise RuntimeError("Wi-Fi connection timed out")

            sleep_ms(250)

    print("Wi-Fi connected:", wlan.ifconfig()[0])
    return wlan


def sync_time():
    ntptime.timeout = 5 # laisser un peu plus de temp pour attendre la reponse de la requête ntp 
    ntptime.settime()  # l'horloge interne est mise à l'heure UTC

    now = localtime()

    print("UTC time: {:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        now[0], now[1], now[2],
        now[3], now[4], now[5]
    ))


def local_time():
    offset_hours = TIMEZONES[tz_index][1]
    return localtime(time() + offset_hours * 3600)


def update_clock():
    now = local_time()
    heure = now[3]
    if Hours_mode == False :
        angle = (heure % 12) * 15
    else :
        angle = (heure % 24) * 7.5
    print("Fuseau:", TIMEZONES[tz_index][0],
          "| Heure: {:02d}:{:02d}".format(now[3], now[4]),
          "| Angle:", angle)
    servo.turn(180 - angle)


connect_wifi()

sync_time()


waiting = False   # un clic est en attente (simple ou double )
last_click = 0
last_press = 0

while True:

    if button.value() == 1 and ticks_diff(ticks_ms(), last_press) > DEBOUNCE_MS:

        now = ticks_ms()

        if waiting and ticks_diff(now, last_click) < double_click:
            print("Double clic")
            Hours_mode = not Hours_mode
            waiting = False
            update_clock()

        else:
            last_click = now
            waiting = True

        last_press = now

        while button.value() == 1:
            sleep_ms(10)

    if waiting and ticks_diff(ticks_ms(), last_click) > double_click:
        print("Simple clic")
        tz_index = (tz_index + 1) % len(TIMEZONES)
        waiting = False
        update_clock()

    if ticks_diff(ticks_ms(), last_update) >= 10000:
        update_clock()
        last_update = ticks_ms()

    sleep_ms(20)