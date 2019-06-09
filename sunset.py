# Tankos, aquarium monitoring and control for MicroPython
# Copyright (c) 2019 Renaud Guillon
# SPDX-License-Identifier: MIT

import logging
import uaiohttpclient as aiohttp

try:
    import json
except ImportError:
    import ujson as json
try:
    import time
except ImportError:
    import utime as time

logger = logging.getLogger("sunset")


def get_current_time_in_seconds():
    return time.time() % (24 * 3600)


def get_ms_until_next_update():
    # return the time in sec until 12AM the next day (UTC time)
    return (24 + 12) * 3600 - get_current_time_in_seconds()


class SunsetTime:
    # The service update will fetch today's sunset time, it shall be called at least once a day. The service get_time
    # will return the number of seconds between now and the sunset time.
    def __init__(self, gps_lat: float, gps_lng: float):
        self.url = 'http://api.sunrise-sunset.org/json?lat=%f&lng=%f&formatted=0' % (
            gps_lat, gps_lng)
        self.sunset_time = 0
        self.last_update_time = 0

    def update(self):
        global logger
        resp = await aiohttp.request("GET", self.url)
        result = await resp.read()
        res = json.loads(result)
        sunset_str = res['results']['sunset'].split(
            'T')[1].split('+')[0].split(':')
        sunset_int = int(sunset_str[0]) * 3600 + \
            int(sunset_str[1]) * 60 + int(sunset_str[2])
        logger.info("New sunset time : %d" % sunset_int)
        self.sunset_time = sunset_int
        self.last_update_time = time.time()

    def get_time(self):
        if self.last_update_time == 0:
            return None
        else:
            return get_current_time_in_seconds() - self.sunset_time

    def get_ms_until_next_update(self):
        return 1000 * ((24+12)*3600 - get_current_time_in_seconds())
