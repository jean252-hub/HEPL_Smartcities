from machine import PWM

class Servo:

    def __init__(self, pin):
        self.pwm = PWM(pin)
        self.pwm.freq(100)

    def turn(self, value):
        duty = int(value / 180 * 13000 + 4000)
        self.pwm.duty_u16(duty)