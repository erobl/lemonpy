from block import Block
import asyncio
from datetime import datetime

# this is a pretty bad clock, I'll figure out how to make a better one later

update_time = 60

class Clock(Block):
    def __init__(self, event):
        super().__init__(event)
        self._cache = self.get_time()

    def get_time(self):
        t = datetime.now()
        return t.strftime("%H:%M:%S")


    async def _thread(self, loop):
        self._cache = self.get_time()
        t = datetime.now()
        await asyncio.sleep(update_time - t.second)
        while True:
            self._cache = self.get_time()
            loop.call_soon_threadsafe(self._event.set)
            # when the computer sleeps
            t = datetime.now()
            await asyncio.sleep(update_time - t.second)
        return
