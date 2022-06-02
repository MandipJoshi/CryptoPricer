#!/usr/bin/python
import os
import discord
import asyncio
import time
import json

from requests import get
from urllib.parse import urljoin

class CoinGecko:
    def __init__(self):
        self.rate_limit = 50
        self.rate_limit_reset = 60
        self.hits = [0, time.time()]
        self.api = "https://api.coingecko.com/api/v3/"

    def get(self, url, parameters=None):
        if self.is_limited():
            print("Failed to call API.. Rate limit exceeded")
        response = get(url, params=parameters)
        self.hits[0] = self.hits[0] + 1
        if self.hits[1] > 60:
            self.hits[1] = time.time()
        return response

    def is_limited(self):
        hits, htime = self.hits
        if hits >= 50 and (time.time() <= htime + 60):
            return True
        return False

    def _ping(self):
        path = '/ping'
        url = urljoin(self.api, path.lstrip('/'))
        response = self.get(url)
        return response.status_code

    def _price(self, coin, currency):
        path = '/simple/price'
        url = urljoin(self.api, path.lstrip('/'))
        query = {
            'ids' : coin,
            'vs_currencies': currency
        }
        response = self.get(url, parameters=query)
        json_data = json.loads(response.text)
        price = json_data[coin]['usd']
        return price

class CryptoPricer(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = CoinGecko()

    async def timed_updates(self):
        #await self._refresh()
        profit_to_cover = 1.5
        current_money = 18.108
        channel = await self.fetch_channel('981616756407799808')
        baseline_price = 1.002
        price = self.api._price('busd', 'usd')
        if price > baseline_price:
            increase = ((price - baseline_price)/(baseline_price))
            increase_percent = increase * 100
            await channel.send(f"BUSD Price increased by: {round(increase_percent, 2)}%. Original Price: {baseline_price}, Current Price: {price}")
            await channel.send(f"Current BUSD: {current_money}, BUSD after exchange: {round(current_money + increase * current_money, 2)}")
        elif price < baseline_price:
            decrease = ((baseline_price - price)/(baseline_price))
            decrease_percent = decrease * 100
            await channel.send(f"BUSD Price decreased by: {round(decrease_percent, 2)}%. Original Price: {baseline_price}, Current Price: {price}")
            await channel.send(f"Current BUSD: {current_money}, BUSD after exchange: {round(current_money - decrease * current_money, 2)}")
        await asyncio.sleep(300)

    async def _price(self, message):
        if not ' ' in message.content:
            await message.channel.send(f"Enter the coin the you want the price of!")
            return
        else:
            coin = message.content.split(' ')[-1]
        price = self.api._price(coin, 'usd')
        await message.channel.send(f"**{coin.capitalize()} Price**: ${price}")

    async def _refresh(self):
        refresh = self.api._price('bitcoin', 'usd')
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=refresh))

    async def on_message(self, message):
        if message.author == self.user:
            return
        msg = message.content
        if msg.startswith('~'):
            command = msg.split(' ')[0].replace('~', '_') if ' ' in msg else msg.replace('~', '_')
            await getattr(self, command)(message)

    async def on_ready(self):
        print(f"Logged in as: {self.user.name}({self.user.id})")
        print(f"Bot API Status: {self.api._ping()}")
        self.loop.create_task(self.timed_updates())

client = CryptoPricer()
client.run(os.getenv("TOKEN"))
