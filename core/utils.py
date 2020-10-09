from discord.ext.commands import Bot, Context

def early_return(bot, ctx:Context):
    """ returns 'True' if author equals user """
    return ctx.message.author.bot or ctx.message.author.id == bot.user.id