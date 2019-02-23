#!/usr/bin/env python3
import asyncio

from asyncio import Event
from i3 import i3block
from clock import Clock
from battery import Battery

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

async def input(loop):
    bar = await create_bar()
    update_bar = Event()

    modules = { "l": [], "c": [], "r": [] } 

    modules["l"].append(Clock(update_bar))
    modules["c"].append(i3block(update_bar))
    modules["r"].append(Battery(update_bar, 1))

    for m in modules:
        for b in modules[m]:
            asyncio.run_coroutine_threadsafe(b.start(loop), loop)

    async def output():
       while True:
           command = (await bar.stdout.readline()).decode().strip()
           print(command)

    asyncio.run_coroutine_threadsafe(output(), loop)

    while True:
        output = ""
        for m in modules:
            output += "%%{%s}" % m
            for b in modules[m]:
                output += b.stringval()
        bar.stdin.write(bytes(output, 'utf8') + b'\n')
        await update_bar.wait()
        update_bar.clear()


loop = asyncio.get_event_loop()
loop.run_until_complete(input(loop))

