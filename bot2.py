#!/usr/bin/python
import discord

def get_price():
    response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
    json_data = json.loads(response.text)
    price = json_data['bitcoin']['usd']
    return (price)

class CryptoPricer(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def price(self, message):
        price = get_price()
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
        print(f'{self.color.good} Logged in as: {self.user.name}({self.user.id})')


client = CryptoPricer()
