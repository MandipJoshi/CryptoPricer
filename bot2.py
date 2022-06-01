#!/usr/bin/python
import discord
from urllib.parse import urljoin

class CoinGecko:
    def __init__(self):
        self.rate_limit = 50
        self.rate_limit_reset = 60
        self.hits = (0, 0.0)
        self.api = "https://api.coingecko.com/api/v3/simple/"

    def is_limited(self):
        hits, time = self.hits
        if hits => 50 and int(time) <= 60:
            return False
        return True

    def _ping(self):
        path = '/ping'
        url = urljoin(self.api + path.lstrip('/'))
        response = requests.get(url)
        print(r.status)

    def _price(self, coin, currency):
        path = '/price'
        url = urljoin(self.api + path.lstrip('/'))
        query = {
            'ids' : coin,
            'vs_currencies': currency
        }
        response = requests.get(url, params=query)
        json_data = json.loads(response.text)
        price = json_data['bitcoin']['usd']
        return price

class CryptoPricer(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = CoinGecko()

    async def price(self, message):
        price = self.api._price('bitcoin', 'usd')
        await message.channel.send(f"**Bitcoin Price**: ${price}")

    async def refresh(self):
        refresh = get_price()
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"${refresh}"))

    async def on_message(self, message):
        if message.author == self.user:
            return
        msg = message.content
        if message.startswith('~'):
            getattr(self, message[1:])()

    async def on_ready(self):
        print(f"Logged in as: {self.user.name}({self.user.id})")
        print(f"Bot API Status: {self.api.ping}")

client = CryptoPricer()
