import re

from discord.ext.commands import Bot, Context

def early_return(bot:Bot, ctx:Context):
    """returns 'True' if author is himself or a bot"""
    return ctx.message.author.bot or ctx.message.author.id == bot.user.id

async def help_wrapper(bot:Bot, ctx:Context):
    """References the doc"""
    await self.bot.sendf(ctx, title="Use `{0}help {1}`".format(ctx.prefix, ctx.invoked_with))

def get_last_number(s:str):
    """Returns the last integer found in a string (-1 if none)"""
    array = re.findall(r'[0-9]+', s)
    if array.__len__() is 0:
        return -1
    return int(array[-1])
