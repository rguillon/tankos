import setup
from machine import Pin, PWM
from sunset import SunsetTime
from dimmer import Dimmer
import time


class PWMOutput:

    PWM_MAX=1024.0

    def __init__(self, pwm):
        self.pwm = pwm

    def set(self, value):
        print("Value to set: %f"%value)
        self.pwm.duty(int(value * self.PWM_MAX))


pwm1 = PWM(Pin(2, Pin.OUT))
pwm2 = PWM(Pin(0, Pin.OUT))
pwmWhite = PWMOutput(pwm1)
pwmBlue = PWMOutput(pwm2)
time_src = SunsetTime()

time_src.update()

dimmerWhite = Dimmer(time_src, pwmWhite, [ [0,0],[100000,1]])
dimmerBlue  = Dimmer(time_src, pwmBlue, [ [0,0],[100000,1]])


setup.do_setup()

while True:
    dimmerWhite.update()
    dimmerBlue.update()

    time.sleep_ms(10)
