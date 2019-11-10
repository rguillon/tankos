# Tanreceive_ckos, aquarium monitoring and control for MicroPython
# Copyright (c) 2019 Renaud Guillon
# SPDX-License-Identifier: MIT

import network
import logging
import ntptime
from machine import Pin, PWM, I2C

import uasyncio as asyncio
import config
from dimmer import Dimmer
from display import Display
from mqtt_logs import MqttLogs
from sunset import SunsetTime
from time_sync import TimeSync
from wdt import Wdt

import mqtt_as

mqtt_client = None


tasks = {}


class PWMOutput:
    # adapter class between the Dimmer and the PWM output
    PWM_MAX = 1023.0

    def __init__(self, pwm):
        self.pwm = pwm

    def set(self, value):
        self.pwm.duty(int(value * self.PWM_MAX))


pwm1 = PWM(Pin(12, Pin.OUT))
pwm2 = PWM(Pin(13, Pin.OUT))
pwm3 = PWM(Pin(14, Pin.OUT))
i2c = I2C(-1, Pin(18, Pin.OUT), Pin(19, Pin.OUT))


mqtt = None

def init():
    # Factory function that intantiates and configure the tasks
    global tasks, pwm1, pwm2, i2c

    #sta_if = network.WLAN(network.STA_IF)
    #if not sta_if.isconnected():
    #    print('connecting to network...')
    #    sta_if.active(True)
    #    sta_if.connect(config.wlan_ssid, config.wlan_pass)
    #    while not sta_if.isconnected():
    #        pass

    # Default "do little" coro for optional user replacement
    async def eliza(*_):  # e.g. via set_wifi_handler(coro): see test program
        await asyncio.sleep_ms(20)

    conf = {
        'client_id': "123456778",
        'server': "192.168.1.200",
        'port': 0,
        'user': '',
        'password': '',
        'keepalive': 60,
        'ping_interval': 0,
        'ssl': False,
        'ssl_params': {},
        'response_time': 10,
        'clean_init': True,
        'clean': True,
        'max_repubs': 4,
        'will': None,
        'subs_cb': lambda *_: None,
        'wifi_coro': eliza,
        'connect_coro': eliza,
        'ssid': "Livebox-5B00",
        'wifi_pw': "12345678",
    }

    global mqtt_client
    mqtt_client = mqtt_as.MQTTClient(conf)

    sunset = SunsetTime(con = mqtt_client, gps_lat=config.gps_lat, gps_lng=config.gps_lng)
    time_sync = TimeSync(mqtt_client, i2c)
    mqtt_logs = MqttLogs(
        mqtt_client=mqtt_client, topic="tankos/logs/", max_msg=100)

    cold_white_schedule = [[-3600*2, 0], [-3600, 1.0], [3600*5, 0.8], [3600*6, 0]]
    warm_white_schedule = [[-3600*2, 0], [-3600, 1.0], [3600*4, 1.0], [3600*5, 0]]
    
    white_schedule = [[-3600*2, 0], [-3600, 0.6], [3600*4, 0.8], [3600*5, 0]]
    
    cold_white_dimmer = Dimmer("cold_white", sunset, PWMOutput(pwm2), cold_white_schedule)
    warm_white_dimmer = Dimmer("warm_white", sunset, PWMOutput(pwm3), warm_white_schedule)
    white_dimmer = Dimmer("while", sunset, PWMOutput(pwm1), white_schedule)
    display = Display(i2c, [white_dimmer],sunset)
    #wdt = Wdt()

    global tasks
    tasks["01_mqtt_logs"] = mqtt_logs
    tasks["02_time_syn"] = time_sync
    tasks["03_sunset"] = sunset
    tasks["04_cold_while_dimmer"] = cold_white_dimmer
    tasks["05_warm__dimmer"] = warm_white_dimmer
    tasks["06_while_dimmer"] = white_dimmer
    tasks["06_display"] = display

   # tasks["wdt"] = Wdt()

    logging.basicConfig(level=logging.INFO, filename=None,
                        stream=mqtt_logs, format=None)
