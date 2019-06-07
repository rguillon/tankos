import config
import time
import http_client
try:
    import json
except ImportError:
    import ujson as json
try:
    import time
except ImportError:
    import utime as time


def get_sunset_time_in_seconds():
    result = json.loads(http_client.get(
        'https://api.sunrise-sunset.org/json?lat=%f&lng=%f&formatted=0'%(config.gps_lat,
            config.gps_lng)).text)
    sunset_str = result['results']['sunset'].split(
        'T')[1].split('+')[0].split(':')
    sunset_int = int(sunset_str[0]) * 3600 + \
        int(sunset_str[1])*60 + int(sunset_str[2])
    return sunset_int


def get_current_time_in_seconds():
    lt = time.localtime()

    return lt[3]*3600 + lt[4]*60 + lt[5]



class SunsetTime:
    def __init__(self, update_period = 23*3600):
        self.sunset = 0
        self.update_period = update_period
        self.last_update_time = 0


    def update(self):
        t = time.time()
        if t - self.last_update_time > self.update_period:
            self.sunset = get_sunset_time_in_seconds()
            self.last_update_time = t

    def getTime(self):
        return get_current_time_in_seconds() - self.sunset
