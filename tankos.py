import system
import time

def run():

    system.init()



    while True:
        for i  in system.inputs.values():
            i.update()

        for o in system.outputs.values():
            o.update()

        time.sleep_ms(10)
