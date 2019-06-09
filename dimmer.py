# Tankos, aquarium monitoring and control for MicroPython
# Copyright (c) 2019 Renaud Guillon
# SPDX-License-Identifier: MIT

import logging

logger = logging.getLogger("Dimmer")


class Dimmer:
    # Output dimmer, takes a time source, a time table. The service update will
    # interpolate the output value from the table and the current time
    # A safe output value allows to set a default value in case the time is not available
    def __init__(self, name, timer, output, time_table, safe_output=0.0):
        self.name = name
        self.timer = timer
        self.output = output
        self.time_table = time_table
        self.time_table.sort()
        self.safe_output = safe_output

    def update(self):
        global logger
        v = 0.0
        t = self.timer.get_time()
        if t is not None:
            if t <= self.time_table[0][0]:
                v = self.time_table[0][1]
            elif t < self.time_table[-1][0]:
                for i in range(1, len(self.time_table)):
                    if t <= self.time_table[i][0]:
                        t1, v1 = self.time_table[i - 1]
                        t2, v2 = self.time_table[i]
                        v = v1 + float(v2 - v1) * (t - t1) / float(t2 - t1)
                        break
            else:
                v = self.time_table[-1][1]
        else:
            v = self.safe_output

        logger.info("Dimmer %s set %f at time %d" % (self.name, v, t))
        self.output.set(v)

    def get_ms_until_next_update(self):
        return 1000
