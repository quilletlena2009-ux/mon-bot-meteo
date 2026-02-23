import discord
from discord.ext import tasks, commands
import datetime
import random
import os
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "Bot en ligne !"
def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive():
    t = Thread(target=run)
    t.start()

TOKEN = os.getenv('TOKEN')
CHANNEL_ID = 1422958632395341875

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        self.weather_task.start()

    @tasks.loop(time=datetime.time(hour=8, minute=0, second=0))
    async def weather_task(self):
        channel = self.get_channel(CHANNEL_ID)
        if channel:
            msg, img = self.get_random_meteo()
            embed = discord.Embed(title="Météo du jour", description=msg, color=0x3498db)
            embed.set_image(url=img)
            await channel.send(embed=embed)

    @commands.command(name="meteo")
    async def meteo(self, ctx):
        msg, img = self.get_random_meteo()
        embed = discord.Embed(title="Météo demandée", description=msg, color=0x3498db)
        embed.set_image(url=img)
        await ctx.send(embed=embed)

    def get_random_meteo(self):
        options = [
            ("Le soleil brille sur Poudlard! ☀️", "https://cdn.discordapp.com/attachments/1362231762197156264/1474885740683989012/image.png?ex=699d7422&is=699c22a2&hm=c4585412a1b49b911d96ebece9f3f4e200c6cb2ac94fb4562f5d11519f440ebf"),
            ("Il y a pas mal de vent aujourd'hui... 💨", "https://media.discordapp.net/attachments/1362231762197156264/1474885907512295464/image.png?ex=699d744a&is=699c22ca&hm=874ff357ad5b00fbd05487ad75db3c661aa936daecc2ec5b4f37078e411acbab"),
            ("Le ciel d'Ecosse est très nuageux. ☁️", "https://media.discordapp.net/attachments/1362231762197156264/1474886005239840890/image.png?ex=699d7461&is=699c22e1&hm=d56a23f58df3385cc7fadd227da5849c3c38ac3d35f8ef3e7858dcb87bb94987"),
            ("Prévoyez le parapluie, il pleut sur le château. 🌧️", "https://media.discordapp.net/attachments/1362231762197156264/1474885824188383294/image.png?ex=699d7436&is=699c22b6&hm=43e00f1c8cdc2817e6138642befc61d1d235786a2ef623e54581a63a2d970af2"),
            ("ALERTE ORAGE ! Restez à l'abri. ⚡", "https://media.discordapp.net/attachments/1362231762197156264/1474886156515803247/image.png?ex=699d7485&is=699c2305&hm=18c84f2de7f18e0383be6dae4a618540eeabfcf1847c8c0889bf0d82313348f3")
        ]
        return random.choice(options)

bot = MyBot()
keep_alive()
bot.run(TOKEN)
