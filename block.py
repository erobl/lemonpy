from abc import ABC, abstractmethod
from threading import Thread

class Block(ABC):
    def __init__(self, event):
        self._cache = ""
        self._event = event
        return

    @abstractmethod
    def _thread(self):
        pass

    def start(self):
        # run self._thread in another thread
        t = Thread(target=self._thread)
        t.start()
        return

    def stringval(self):
        return self._cache

