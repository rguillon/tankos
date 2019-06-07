import config
import network
import ntptime

from machine import Pin, PWM
from sunset import SunsetTime
from dimmer import Dimmer

from umqtt.robust import MQTTClient

mqtt_client = None

outputs = {}

inputs = {}

class PWMOutput:

    PWM_MAX=1024.0

    def __init__(self, pwm):
        self.pwm = pwm

    def set(self, value):
        print("Value to set: %f"%value)
        self.pwm.duty(int(value * self.PWM_MAX))



def publish(topic, msg):
     mqtt_client.publish(topic, msg)



def init():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config.wlan_ssid, config.wlan_pass)
        while not sta_if.isconnected():
            pass

    ntptime.settime()

    global mqtt_client
    mqtt_client = MQTTClient("tankos_client", config.mqtt_broker)
    mqtt_client.connect()


    pwm1 = PWM(Pin(2, Pin.OUT))
    pwm2 = PWM(Pin(0, Pin.OUT))

    global inputs
    inputs["time"] =  SunsetTime()

    global outputs
    outputs["white_dimer"] = Dimmer(inputs["time"], PWMOutput(pwm1), [ [0,0],[100000,1]])
    outputs["blue_dimmer"] = Dimmer(inputs["time"], PWMOutput(pwm2), [ [0,0],[100000,1]])



#    while True:
#        dimmerWhite.update()
#        dimmerBlue.update()
#        print(gc.mem_free())
#        time.sleep_ms(10)

