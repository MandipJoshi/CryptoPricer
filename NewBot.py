#!/usr/bin/python
import os
import discord
import asyncio
import time

from requests import get
from urllib.parse import urljoin

class CoinGecko:
    def __init__(self):
        self.rate_limit = 50
        self.rate_limit_reset = 60
        self.hits = (0, time.time())
        self.api = "https://api.coingecko.com/api/v3/simple/"

    def get(self, url, parameters=None):
        if self.is_limited():
            print("Failed to call API.. Rate limit exceeded")
        r = get(url, params=parameters)
        self.hits[0] = self.hits[0] + 1
        if self.hits[1] > 60:
            self.hits[1] = time.time()

    def is_limited(self):
        hits, htime = self.hits
        if hits >= 50 and (time.time() <= htime + 60):
            return False
        return True

    def _ping(self):
        path = '/ping'
        url = urljoin(self.api + path.lstrip('/'))
        response = self.get(url)
        print(r.status)

    def _price(self, coin, currency):
        path = '/price'
        url = urljoin(self.api + path.lstrip('/'))
        query = {
            'ids' : coin,
            'vs_currencies': currency
        }
        response = self.get(url, parameters=query)
        json_data = json.loads(response.text)
        price = json_data['bitcoin']['usd']
        return price

class CryptoPricer(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop.create_task(self.timed_updates())
        self.api = CoinGecko()

    async def timed_updates(self):
        self._refresh()
        await asyncio.sleep(300)

    async def _price(self, message):
        price = self.api._price('bitcoin', 'usd')
        await message.channel.send(f"**Bitcoin Price**: ${price}")

    async def _refresh(self):
        refresh = self.api._price('bitcoin', 'usd')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"${refresh}"))

    async def on_message(self, message):
        if message.author == self.user:
            return
        msg = message.content
        if message.startswith('~'):
            getattr(self, message.replace('~', '_'))()

    async def on_ready(self):
        print(f"Logged in as: {self.user.name}({self.user.id})")
        print(f"Bot API Status: {self.api.ping}")

client = CryptoPricer()
client.run(os.getenv("TOKEN"))