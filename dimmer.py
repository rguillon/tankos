
import logging

logger= logging.getLogger("Dimmer")

class Dimmer:
    def __init__(self, timer, output, time_table):
        self.timer = timer
        self.output = output
        self.time_table = time_table
        self.time_table.sort()


    def update(self):
        global logger
        t = self.timer.getTime()
        v=0.0
        if t <= self.time_table[0][0]:
            v = self.time_table[0][1]
        elif t< self.time_table[-1][0]:
            for i in range(1, len(self.time_table)):
                if t <=  self.time_table[i][0]:
                    t1, v1 = self.time_table[i-1]
                    t2, v2 = self.time_table[i]
                    v = v1 + float(v2-v1)*(t-t1)/float(t2-t1)
                    self.output.set(v)
        else:
            v = self.time_table[-1][1]
        logger.info("value set %f at time %d"%(v,t))
        self.output.set(v)

