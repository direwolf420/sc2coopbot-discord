import ast
import math
import sys
import re

import urllib.parse
import urllib.request

#import aiohttp

import core.consts as consts
import core.caches as cc

from core.caches import Commander, Map
from core.field import Field
from core.requests import RequestHandler, RequestType

from discord.ext.commands import Bot, Cog, Context, Command, command
from discord.embeds import Embed
from discord.colour import Colour

class Commanders(Cog):

    def __init__(self, bot:Bot):
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

def setup(bot:Bot):
    bot.add_cog(Commanders(bot))