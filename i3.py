from block import Block
from symbols import symbols
import i3ipc

class i3block(Block):
    def __init__(self, event):
        super().__init__(event)
        self._i3conn = i3ipc.Connection()

    def _thread(self):
        def on_workspace_focus(conn, e):
            ws = conn.get_workspaces()
            output = self.draw_workspaces(ws)
            # send it to main thread
            self._cache = output
            self._event.set()
        self._i3conn.on('workspace::focus', on_workspace_focus)
        self._i3conn.main()

    def draw_workspaces(self, ws):
        warr = [symbols["empty_workspace"] for i in range(10)]
        for w in ws:
            wval = ""
            if w["urgent"]:
                wval += "%{F#FF0000}"
            if w["focused"]:
                wval += "%{F#0000FF}"
            wval += symbols["workspace"]
            if w["focused"] or w["urgent"]:
                wval += "%{F-}"
            warr[w["num"] - 1] = wval
        output = " ".join(warr)
        return output
