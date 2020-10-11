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

    @command()
    async def honk(self, ctx:Context):
        if ut.early_return(self.bot, ctx):
            return

        await self.bot.sendf(ctx, image_url=consts.HONK_URL)

        
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