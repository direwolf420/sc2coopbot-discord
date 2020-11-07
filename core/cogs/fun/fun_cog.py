import ast
import math
import sys
import re
import random

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
        """honk"""
        if ut.early_return(self.bot, ctx):
            return

        await self.bot.sendf(ctx, image_url=consts.HONK_URL)

    @command(aliases=["i", "fun", "f"])
    async def image(self, ctx:Context, *args):
        """
        Random commander related images

        Possible args:
        * commanderalias
          -> Lists all keywords for a commander
        * commanderalias + keyword
          -> Returns an image associated with that keyword

        Basic usage:
        >>> [prefix]fun karax wide -> Funny image of a wide karax
        """
        if ut.early_return(self.bot, ctx):
            return

        count = args.__len__()
        sargs = [a.lower() for a in args] # sanitize to lowercase only
        if count == 0:
            await ut.help_wrapper(self.bot, ctx)
            return

        alias = sargs[0]

        if alias in ("h", "help"):
            await ut.help_wrapper(self.bot, ctx)
            return

        comm = Commander.from_alias(alias)

        if comm is None:
            await self.bot.sendf(ctx, title=consts.ERR_STR, description="No commander with alias '{}' found!".format(alias))
            return

        queryType = RequestType.NONE

        if count == 1:

            if not comm.has_fun:
                await self.bot.sendf(ctx, title=consts.ERR_STR, description="'{}' has no images yet!".format(comm.display_name))
                return

            fun_count = comm.fun.__len__()

            fields = ()
            first_half = "```"
            sec_half = "```"
            half = fun_count // 2
            c = 0
            for keyword in comm.fun:
                format = "\r\n{}".format(keyword)
                if c < half or fun_count == 1:
                    first_half += format
                    c += 1
                else:
                    sec_half += format

            first_half += "```"
            sec_half += "```"

            fields = (Field("Available Images (1/2)", first_half), Field("(2/2)", sec_half))

            if fun_count == 1:
                fields = (Field("Available Images", first_half),)

            footer = "Example: Use \"{0}{1} karax wide\" to get a funny image of a wide karax".format(ctx.prefix, ctx.invoked_with)

            await self.bot.sendf(ctx, fields=fields, footer=footer)
            return

        if count >= 2:
            keyword = sargs[1]

            if keyword in comm.fun:
                url = "{0}/commanderimages/fun/{1}_{2}.png".format(consts.REPO_RAW_URL, comm.name, keyword)
                await self.bot.sendf(ctx, colour=comm.colour, image_url=url)
                return

            else:
                #await self.bot.sendf(ctx, title=consts.ERR_STR, description="Not a supported keyword: {}".format(keyword))
                return
                

        
    @command(aliases=["pong", "p"])
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