from machine import Pin
from machine import ADC
from utime import sleep
ROTARY_ANGLE_SENSOR = ADC(0)


print("LED starts flashing...")
while True:
    print(ROTARY_ANGLE_SENSOR.read_u16())
    sleep(1)
