#!/usr/bin/env python

import discord
import subprocess
import re
import signal
import os

class Client(discord.Client):
    async def on_ready(self):
        print('Logged in as ', self.user)

    async def on_message(self, message):
        for embed in message.embeds:
            # Checking if a valid embed is present
            if embed.video == discord.Embed.Empty:
                return

            # This will run ffprobe each frame extracting the resolution of each frame
            string = 'ffprobe -v error -show_entries frame=width,height -select_streams v -of csv=p=0 -i'
            cmd = string.split(' ')

            # Grabing the url either from discords cache or absolute url
            if embed.video.proxy_url != discord.Embed.Empty:
                cmd.append(embed.video.proxy_url)
            elif embed.video.url != discord.Embed.Empty:
                cmd.append(embed.video.url)
            else:
                return

            start_resolution = ''
            
            with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP + subprocess.HIGH_PRIORITY_CLASS) as p:
                for line in p.stdout:
                    # Yields the frame resolutions in the format x,y
                    find = re.match(b'([0-9]+),([0-9]+)', line)

                    if find == None:
                        continue

                    # Extract tuple: (b'500', b'200')
                    find = find.groups()

                    if start_resolution == '':
                        start_resolution = find

                    # If new frame does not match start_resolution safe to assume maniuplation of the image and highly likely a crasher
                    if find != start_resolution:
                        p.send_signal(signal.CTRL_BREAK_EVENT)
                        await delete_message(message)

async def delete_message(message):
    try:
        await message.delete()
    except:
        pass

    return

if __name__ == '__main__':
    client = Client()
    client.run(os.environ['TOKEN'])
