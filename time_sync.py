# Tankos, aquarium monitoring and control for MicroPython
# Copyright (c) 2019 Renaud Guillon
# SPDX-License-Identifier: MIT

import time
import ntptime

import ds3231_port
import logging

logger = logging.Logger("time_sync")


class TimeSync():

    def __init__(self, con, i2c):
        try :
            self.ext_rtc = ds3231_port.DS3231(i2c)
        except ds3231_port.DS3231Exception:
            self.ext_rtc = None
        self.con = con

    async def update(self):
        global logger

        if self.ext_rtc is not None:
            t = self.ds3231.get_time(set_rtc = True)
            logger.info("Updating internal RTC %s with external one %s" %
                        (time.localtime(), t))
        try:
            if self.con.isconnected():
                ntptime.settime()
                if self.ext_rtc is not None:
                    self.ext_rtc.save_time()
                logger.info("RTC updated according to NTP")
        except IndexError as e:
            logger.warning("NTP sync failed")
            pass

    def get_ms_until_next_update(self):
        return ((24 + 10) * 3600000) - 1000 * time.time() % (24 * 3600)
