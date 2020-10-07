from discord.ext.commands import Bot
from discord.ext.commands import Context
from discord.ext.commands import Command
from discord.embeds import Embed
from discord.colour import Colour

from discord import Game
import discord

from core.botcommands import BotCommands
import core.consts as consts

from core.field import Field

description = '''A bot that fetches various information about StarCraft 2 Coop mode. Your number two source of coop information'''

# Context doc: https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#context

class CustomBot(Bot):
    """A bot that fetches various information about StarCraft 2 Coop mode. Your number two source of coop information"""
    def __init__(self, release:bool, **options):
        if release:
            prefix = consts.PREFIX
        else:
            prefix = consts.PREFIX_DEBUG
        super().__init__(command_prefix=prefix,
                         description=description,
                         case_insensitive=True,
                         activity=Game(name="{0} | {1}".format(prefix, consts.SC2COOP_URL)),
                         **options)
        self.bot_commands = BotCommands(self)
        self.bot_commands.add_commands()

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")
        print("Logged in as")
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        if message.mentions.__len__() is 1 and self.user in message.mentions:
            # if mentioned, and the only mention, give back the prefix
            prefix = str(await self.get_prefix(message))
            return await message.channel.send(content="Hi, my prefix is `{}`".format(prefix))
        await super().on_message(message)

    
    async def sendf(self, ctx:Context, description=None, fields:tuple=(), author:tuple=(), image_url:str=None, title:str=None, colour:Colour=None, footer:bool=False):
        """Formats into an embed and sends it"""
        embed = Embed()
        if colour is None:
            embed.colour = Colour.dark_grey()
        else:
            embed.colour = colour
        embed.title = title
        embed.description = description
        if author.__len__() >= 2:
            embed.set_author(name=str(author[0]), icon_url=str(author[1]))

        if fields.__len__() > 0:
            if type(fields[0]) is Field:
                for field in fields:
                    embed.add_field(name=field.name, value=field.value, inline=True)

        if footer:
            author = ctx.message.author
            embed.set_footer(text="Requested by {}, Powered by Starcraft2Coop.com".format(author), icon_url=ctx.message.author.avatar_url)

        if image_url is not None:
            embed.set_image(url=image_url)
        
        await ctx.send(embed=embed)
        #file = discord.File("stukov.png", filename="stukov.png")
        #await ctx.send(embed=embed, file=file)
