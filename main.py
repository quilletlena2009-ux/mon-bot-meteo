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
CHANNEL_ID = 1422958632395341875 

class MyBot(commands.Bot):
    def __init__(self):
        # Activation des intents essentiels
        intents = discord.Intents.default()
        intents.message_content = True 
        intents.members = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Lancement de la tâche automatique
        self.weather_task.start()

    @tasks.loop(time=datetime.time(hour=8, minute=0, second=0))
    async def weather_task(self):
        channel = self.get_channel(CHANNEL_ID)
        if channel:
            meteo_options = [
                {"msg": "Le soleil brille sur Poudlard! ☀️", "img": "https://cdn.discordapp.com/attachments/1362231762197156264/1474885740683989012/image.png?ex=699d7422&is=699c22a2&hm=c4585412a1b49b911d96ebece9f3f4e200c6cb2ac94fb4562f5d11519f440ebf"},
                {"msg": "Il y a pas mal de vent aujourd'hui... 💨", "img": "https://media.discordapp.net/attachments/1362231762197156264/1474885907512295464/image.png?ex=699d744a&is=699c22ca&hm=874ff357ad5b00fbd05487ad75db3c661aa936daecc2ec5b4f37078e411acbab&=&format=webp&quality=lossless&width=573&height=801"},
                {"msg": "Le ciel d'Ecosse est très nuageux. ☁️", "img": "https://media.discordapp.net/attachments/1362231762197156264/1474886005239840890/image.png?ex=699d7461&is=699c22e1&hm=d56a23f58df3385cc7fadd227da5849c3c38ac3d35f8ef3e7858dcb87bb94987&=&format=webp&quality=lossless&width=573&height=801"},
                {"msg": "Prévoyez le parapluie, il pleut sur le château. 🌧️", "img": "