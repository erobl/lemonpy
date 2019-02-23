from block import Block
import asyncio
from symbols import symbols
import os

class Battery(Block):
    def __init__(self, event, interval):
        super().__init__(event)
        self.interval = interval
        self._cache = self.get_battery()

    def read_bat(self, bat):
        # I have a weird battery so I can't use psutil
        path = os.path.join("/sys/class/power_supply", bat)
        with open(os.path.join(path, "energy_now")) as f:
            for line in f:
                energy_now = int(line)

        with open(os.path.join(path, "energy_full")) as f:
            for line in f:
                energy_full = int(line)

        return energy_now/energy_full

    def read_charging(self):
        path = "/sys/class/power_supply/AC/online"
        with open(path) as f:
            for line in f:
                return int(line)

        

    def get_battery(self):
        bat0 = self.read_bat("BAT0")
        bat1 = self.read_bat("BAT1")
        bat_avg = int(100 * (bat0 + bat1)/2)
        charging = self.read_charging()

        icon = ""
        if charging == 1:
            icon = symbols["charging"]
        elif bat_avg > 80:
            icon = symbols["battery4"]
        elif bat_avg > 60:
            icon = symbols["battery3"]
        elif bat_avg > 40:
            icon = symbols["battery2"]
        elif bat_avg > 20:
            icon = symbols["battery1"]
        else:
            icon = symbols["battery0"]

        return "%s %d%%" % (icon, bat_avg)

    async def _thread(self, loop):
        self._cache = self.get_battery()
        while True:
            await asyncio.sleep(self.interval)
            self._cache = self.get_battery()
            loop.call_soon_threadsafe(self._event.set)
