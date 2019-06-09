# Tankos, aquarium monitoring and control for MicroPython
# Copyright (c) 2019 Renaud Guillon
# SPDX-License-Identifier: MIT

import time
import ssd1306


class Display():
    def __init__(self, i2c):
        self.ssd1306 = ssd1306.SSD1306_I2C(width=128, height=64, i2c=i2c)
        self.init_t = time.time()

    def update(self):
        yield
        lt = time.localtime()
        t = time.time()
        self.ssd1306.fill(0)

        self.ssd1306.text("%d/%d/%d %d:%d:%d" %
                          (lt[0] % 100, lt[1], lt[2], lt[3], lt[4], lt[5]), 0, 0)
        self.ssd1306.text("up:%d" % (t - self.init_t), 0, 16)

        self.ssd1306.show()

    def get_ms_until_next_update(self):
        return 1000
