# Tankos, aquarium monitoring and control for MicroPython
# Copyright (c) 2019 Renaud Guillon
# SPDX-License-Identifier: MIT

from machine import WDT

class Wdt():
    def __init__(self, period_ms = 1000):
        self.period_ms = period_ms
        self.wdt = WDT(timeout = self.period_ms * 2)

    def update(self):
        self.wdt.feed()

    def get_ms_until_next_update(self):
        return self.period_ms


