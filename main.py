#!/usr/bin/env python3
import asyncio

from threading import Event
from i3 import i3block

async def create_bar():
    args = [
                "lemonbar", '-p',
                '-B', "#FF222222",
                '-F', "#FFFFFFFF",
                '-f', "Roboto Medium:size=12",
                '-f', "System San Francisco Display:size=12:weight=bold",
                '-f', "FontAwesome:size=13"
            ]

    bar = await asyncio.create_subprocess_exec(*args, 
            stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE)
    return bar

async def run():
    bar = await create_bar()
    update_bar = Event()

    modules = { "l": [], "c": [], "r": [] } 

    modules["c"].append(i3block(update_bar))

    for m in modules:
        for b in modules[m]:
            b.start()

    while True:
        update_bar.wait()
        update_bar.clear()
        output = ""
        for m in modules:
            output += "%%{%s}" % m
            for b in modules[m]:
                output += b.stringval()
        bar.stdin.write(bytes(output, 'utf8') + b'\n')

loop = asyncio.get_event_loop()
loop.run_until_complete(run())

