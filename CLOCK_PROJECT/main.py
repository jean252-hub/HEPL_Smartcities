import network
import ntptime

from machine import Pin
from utime import sleep_ms, ticks_ms, ticks_diff, localtime, time
from servo import Servo

from wifi_setup import WIFI_SSID,WIFI_PASSWORD,WIFI_TIMEOUT_MS


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
    ntptime.settime()

    now = localtime()

    print("UTC time: {:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}".format(
        now[0], now[1], now[2],
        now[3], now[4], now[5]
    ))


connect_wifi()
sync_time()

servo = Servo(Pin(20))

def paris_time():
    timestamp = time()

    # UTC + 1 (heure d'hiver)
    timestamp += 3600

    return localtime(timestamp)
while True:
    now = paris_time()
    heure =  now[3]
    angle = (heure % 12) * 15
    print("Heure:", heure, "Angle:", angle)
    servo.turn(angle)
    sleep_ms(10000)
    