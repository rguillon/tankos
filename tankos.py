import system
import uasyncio as asyncio


async def periodic_task(obj):
    while True:
        try:
            await obj.update()
        except:
            pass
        await asyncio.sleep_ms(obj.get_ms_until_next_update())


def run():
    system.init()

    loop = asyncio.get_event_loop()

    for task in system.tasks.values():
        loop.create_task(periodic_task(task))

    loop.run_forever()
