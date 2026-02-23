import discord
from discord.ext import tasks, commands
import datetime
import random
import os
from flask import Flask
from threading import Thread

# --- PARTIE SERVEUR (HÉBERGEMENT 24/7) ---
app = Flask('')
@app.route('/')
def home():
    return "Bot en ligne !"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- CONFIGURATION DU BOT ---
TOKEN = os.getenv('TOKEN') 
CHANNEL_ID = 1234567890 # <--- N'oublie pas de mettre ton ID ici

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # La tâche se lancera chaque jour à 09:00:00 (Heure UTC par défaut)
        self.weather_task.start()

    @tasks.loop(time=datetime.time(hour=8, minute=0, second=0))
    async def weather_task(self):
        channel = self.get_channel(CHANNEL_ID)
        if channel:
            # 1. Définition des options
            meteo_options = [
                {"msg": "Le soleil brille sur Poudlard! ☀️", "img": "https://cdn.discordapp.com/attachments/1362231762197156264/1474885740683989012/image.png?ex=699d7422&is=699c22a2&hm=c4585412a1b49b911d96ebece9f3f4e200c6cb2ac94fb4562f5d11519f440ebf"},
                {"msg": "Il y a pas mal de vent aujourd'hui... 💨", "img": "https://media.discordapp.net/attachments/1362231762197156264/1474885907512295464/image.png?ex=699d744a&is=699c22ca&hm=874ff357ad5b00fbd05487ad75db3c661aa936daecc2ec5b4f37078e411acbab&=&format=webp&quality=lossless&width=573&height=801"},
                {"msg": "Le ciel d'Ecosse est très nuageux. ☁️", "img": "https://media.discordapp.net/attachments/1362231762197156264/1474886005239840890/image.png?ex=699d7461&is=699c22e1&hm=d56a23f58df3385cc7fadd227da5849c3c38ac3d35f8ef3e7858dcb87bb94987&=&format=webp&quality=lossless&width=573&height=801"},
                {"msg": "Prévoyez le parapluie, il pleut sur le château. 🌧️", "img":
"https://media.discordapp.net/attachments/1362231762197156264/1474885824188383294/image.png?ex=699d7436&is=699c22b6&hm=43e00f1c8cdc2817e6138642befc61d1d235786a2ef623e54581a63a2d970af2&=&format=webp&quality=lossless&width=570&height=800"},
                {"msg": "ALERTE ORAGE ! Restez à l'abri. ⚡", "img": "https://media.discordapp.net/attachments/1362231762197156264/1474886156515803247/image.png?ex=699d7485&is=699c2305&hm=18c84f2de7f18e0383be6dae4a618540eeabfcf1847c8c0889bf0d82313348f3&=&format=webp&quality=lossless&width=575&height=800"}
            ]

            # 2. Définition des poids (Probabilités)
            # Soleil, Vent, Nuages, Pluie ont un poids de 10 (Chances égales)
            # L'orage a un poids de 2 (5 fois moins de chances)
            poids = [10, 10, 10, 10, 2]

            # 3. Sélection aléatoire pondérée
            # random.choices renvoie une liste, on prend le premier élément [0]
            choice = random.choices(meteo_options, weights=poids, k=1)[0]
            
            embed = discord.Embed(
                title="Météo du jour", 
                description=choice["msg"], 
                color=0x3498db,
                timestamp=datetime.datetime.now()
            )
            embed.set_image(url=choice["img"])
            embed.set_footer(text="Bot Météo Automatique")
            
            await channel.send(embed=embed)

    @weather_task.before_loop
    async def before_weather_task(self):
        await self.wait_until_ready()

bot = MyBot()
keep_alive()
bot.run(TOKEN)