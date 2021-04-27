#!/usr/bin/env python

import discord
import subprocess
import re
import os

class Client(discord.Client):
    async def on_ready(self):
        print('Logged in as ', self.user)

    async def on_message(self, message):
        for embed in message.embeds:
            if embed.video is discord.Embed.Empty:
                return

            string = 'ffprobe -show_entries frame=width,height -select_streams v -of csv=p=0 -i'
            cmd = string.split(' ')

            if embed.video.proxy_url:
                cmd.append(embed.video.proxy_url)
            else:
                cmd.append(embed.video.url)

            frames = {}

            check = run_cmd(cmd)
            if check.returncode == 0:
                find = re.findall(b'[0-9]+,[0-9]+', check.stdout)

                for frame in find:
                    frames.setdefault(frame, 0)
                    frames[frame] += 1

            if len(frames.keys()) > 1:
                try:
                    await message.delete()
                except:
                    pass


def run_cmd(cmd):
    completed = subprocess.run(cmd, capture_output=True)
    return completed


if __name__ == '__main__':
    client = Client()
    client.run(os.environ['TOKEN'])

