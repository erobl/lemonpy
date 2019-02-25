from block import Block
from symbols import symbols
import i3ipc
from color import color

class i3block(Block):
    def __init__(self, event):
        super().__init__(event)
        self._i3conn = i3ipc.Connection()
        ws = self._i3conn.get_workspaces()
        self._cache = self.draw_workspaces(ws)

    async def _thread(self, loop):
        def on_workspace_focus(conn, e):
            ws = self._i3conn.get_workspaces()
            output = self.draw_workspaces(ws)
            # send it to main thread
            self._cache = output
            loop.call_soon_threadsafe(self._event.set)
        self._i3conn.on('workspace::focus', on_workspace_focus)
        loop.run_in_executor(None, self._i3conn.main)

    def draw_workspaces(self, ws):
        warr = [symbols["empty_workspace"] for i in range(10)]
        for w in ws:
            wval = ""
            if "urgent" in w and w["urgent"]:
                wval += "%%{F%s}" % color["urgent"]
            if w["focused"]:
                wval += "%%{F%s}" % color["accent"]
            wval += symbols["workspace"]
            if w["focused"] or w["urgent"]:
                wval += "%{F-}"
            warr[w["num"] - 1] = wval

        warr = [("%%{A:w%d:}" % (i + 1)) + w + "%{A}" for i, w in enumerate(warr)]

        output = " ".join(warr)
        return output
