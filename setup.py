import config

import network
import ntptime


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config.wlan_ssid, config.wlan_pass)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


def do_setup():
    do_connect()
    ntptime.settime()
