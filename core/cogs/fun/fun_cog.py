import ast
import math
import sys
import re

import core.consts as consts
import core.caches as cc
import core.utils as ut

from core.caches import Commander, Map
from core.field import Field
from core.requests import RequestHandler, RequestType
from core.custombot import CustomBot

from discord.ext.commands import Bot, Cog, Context, Command, command
from discord.embeds import Embed
from discord.colour import Colour

class FunCog(Cog, name="Fun"):

    def __init__(self, bot:CustomBot):
        self.bot = bot

    def coinflip(self):
        return random.randint(0, 1)

    @command()
    async def gamble(self, ctx:Context, money:int):
        """Gambles some money."""
        pass

    @command()
    async def gamble2(self, ctx:Context, money:int):
        """Gambles some more money."""
        pass

    @command()
    async def honk(self, ctx:Context):
        if ut.early_return(self.bot, ctx):
            return

        await self.bot.sendf(ctx, image_url="https://ih1.redbubble.net/image.928162828.3517/flat,750x1000,075,f.jpg")

        
    @command(aliases=["pong"])
    async def ping(self, ctx:Context):
        """
        Returns the latency
        If it doesn't respond, the bot is most likely dead
        """
        if ut.early_return(self.bot, ctx):
            return

        response = "Pong!"
        if ctx.invoked_with == "pong":
            response = "Ping!"

        await self.bot.sendf(ctx, "Latency: {}ms".format(math.trunc(self.bot.latency * 1000)), title=response)

def setup(bot:CustomBot):
    cog = FunCog(bot)
    bot.add_cog(cog)