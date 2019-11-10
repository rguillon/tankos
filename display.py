# Tankos, aquarium monitoring and control for MicroPython
# Copyright (c) 2019 Renaud Guillon
# SPDX-License-Identifier: MIT

import time
import ssd1306

class Display():
    def __init__(self, i2c, srcs = None, time = None):
        try :
            self.screen = ssd1306.SSD1306_I2C(width=128, height=64, i2c=i2c)
        except OSError:
            self.screen = None
        self.init_t = 0
        self.srcs = srcs
        self.time = time

    async def update(self):
        if self.init_t == 0:
            self.init_t = time.time()
        t = time.time()
        lt = time.localtime()
        if self.screen is not None:
            self.screen.fill(0)

            self.screen.text("%d/%d/%d %d:%d:%d" %
                              (lt[0] % 100, lt[1], lt[2], lt[3], lt[4], lt[5]), 0, 0)
            self.screen.text("up:%d" % (t - self.init_t), 0, 16)

            if self.srcs is not None:
                y=32
                for src in self.srcs:
                    self.screen.text("%s:%.5f"%(src.name, src.get_value()),0,y)
                    y+=16
            self.screen.text("%d"%( self.time.get_time()),0, 64)
            self.screen.show()

    def get_ms_until_next_update(self):
        return 1000
