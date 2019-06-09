# Tankos, aquarium monitoring and control for MicroPython
# Copyright (c) 2019 Renaud Guillon
# SPDX-License-Identifier: MIT

import time
import machine
import ntptime

import ds3231_port
import logging

logger = logging.Logger("time_sync")


class TimeSync():

    def __init__(self, i2c):
        self.ds3231 = ds3231_port.DS3231(i2c)

    def update(self):
        global logger

        t = self.ds3231.get_time()
        logger.info("Updating internal RTC %s with external one %s" %
                    (time.localtime(), t))
        machine.RTC().datetime(self.ds3231.get_time())
        try:
            ntptime.settime()
            self.ds3231.save_time()
            logger.info("RTC updates according to NTP")

        except IndexError as e:
            logger.warning("NTP sync failed")
            pass

    def get_ms_until_next_update(self):
        return ((24 + 10) * 3600000) - 1000 * time.time() % (24 * 3600)
