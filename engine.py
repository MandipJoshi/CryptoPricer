#!/usr/bin/python
import discord

class CryptoPricer(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_message(self, message):
        pass

    async def on_ready(self):
        print(f'{self.color.good} Logged in as: {self.user.name}({self.user.id})')

