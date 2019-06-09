# Tankos, aquarium monitoring and control for MicroPython
# Copyright (c) 2019 Renaud Guillon
# SPDX-License-Identifier: MIT

import network
import logging
import ntptime
from machine import Pin, PWM, I2C

import config
from dimmer import Dimmer
from display import Display
from mqtt_logs import MqttLogs
from sunset import SunsetTime
from time_sync import TimeSync
from umqtt.robust import MQTTClient


mqtt_client = None


tasks = {}


class PWMOutput:
    # adapter class between the Dimmer and the PWM output
    PWM_MAX = 1024.0

    def __init__(self, pwm):
        self.pwm = pwm

    def set(self, value):
        self.pwm.duty(int(value * self.PWM_MAX))


pwm1 = PWM(Pin(2, Pin.OUT))
pwm2 = PWM(Pin(0, Pin.OUT))
i2c = I2C(-1, Pin(21, Pin.OUT), Pin(22, Pin.OUT))


def init():
    # Factory function that intantiates and configure the tasks
    global tasks, pwm1, pwm2, i2c
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

    tasks["time"] = SunsetTime(gps_lat=config.gps_lat, gps_lng=config.gps_lng)
    tasks["time_sync"] = TimeSync(i2c)
    tasks["mqtt_logs"] = MqttLogs(
        mqtt_client=mqtt_client, topic="tankos/logs/", max_msg=100)

    tasks["white_dimer"] = Dimmer(
        "while", tasks["time"], PWMOutput(pwm1), [[0, 0], [100000, 1]])
    tasks["blue_dimmer"] = Dimmer(
        "blue", tasks["time"], PWMOutput(pwm2), [[0, 0], [100000, 1]])
    tasks["display"] = Display(i2c)

    logging.basicConfig(level=logging.INFO, filename=None,
                        stream=tasks["mqtt_logs"], format=None)
