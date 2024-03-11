#!/usr/bin/env python3

import twitchio
from twitchio.ext import commands
from dotenv import load_dotenv, dotenv_values
import re, os
import asyncio

# Configurações
load_dotenv()

TOKEN = os.getenv("TWITCH_TOKEN")  # Você pode obter isso em https://twitchapps.com/tmi/
CHANNEL = os.getenv("TWITCH_CHANNEL")
TARGET_WORD = "!roll"  # Palavra que você deseja monitorar no vídeo
MESSAGE = "!shop"


# Classe do bot
class Bot(commands.Bot):
    valid = 0

    async def event_ready(self):
        # We are logged in and ready to chat and use commands...
        print(f"Logged in as | {self.nick}")

    async def event_message(self, message):
        if message.echo:
            if re.search(TARGET_WORD, message.content, re.IGNORECASE):
                self.valid = 1
            return

        if re.search("você recebeu", message.content, re.IGNORECASE):
            self.valid = 0
            print("Nova rodada")

        if re.search(
            f"{self.nick}, não é hora de usar esse comando..",
            message.content,
            re.IGNORECASE,
        ):
            print("Ops!")
            self.valid = 0
        message.content = message.content.lower()
        await self.handle_commands(message)

    @commands.command()
    async def roll(self, ctx: commands.Context):
        if self.valid == 0:
            self.valid = 1
            print(ctx.author.name, ctx.message.content)
            await asyncio.sleep(3)
            await ctx.send("!roll")
            print("My roll")


# Inicializando o bot
bot = Bot(
    # nick=USERNAME,
    token=TOKEN,
    initial_channels=[CHANNEL],
    prefix="!",
)


# Conectando e rodando o bot
bot.run()
