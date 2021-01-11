import difflib
import re

from discord.ext.commands import Bot, Context

def early_return(bot:Bot, ctx:Context):
    """returns 'True' if author is himself or a bot"""
    return ctx.message.author.bot or ctx.message.author.id == bot.user.id


async def help_wrapper(bot:Bot, ctx:Context):
    """References the doc"""
    await bot.sendf(ctx, title="Use `{0}help {1}`".format(ctx.prefix, ctx.invoked_with))


def get_last_number(s:str):
    """Returns the last integer found in a string (-1 if none)"""
    array = re.findall(r'[0-9]+', s)
    if array.__len__() is 0:
        return -1
    return int(array[-1])


def seq_to_list_str(input, output):
    """
    if input is str: return

    if input is sequence:
        if element is str: append it to the output
        else: seq_to_list_str(element, output)
    """
    if isinstance(input, str):
        # last recursive call
        return

    for element in input:
        if isinstance(element, str):
            output.append(element)
        else:
            seq_to_list_str(element, output)


def is_subsequence(s1, s2, m, n):
    # base cases
    if m == 0:
        return True
    if n == 0:
        return False

    # if last characters of two strings are matching
    if s1[m-1] == s2[n-1]:
        return is_subsequence(s1, s2, m-1, n-1)

    # if last characters are not matching
    return is_subsequence(s1, s2, m, n-1)


def matching_subsequence_in(s, seq):
    for other in seq:
        if is_subsequence(s, other, len(s), len(other)):
            return other;
    return None;


def get_matches(alias:str, possibilities):
    if len(alias) > 2:
        sequence_match = matching_subsequence_in(alias, possibilities)
        if sequence_match is not None:
            return [sequence_match]

    return difflib.get_close_matches(alias, possibilities, cutoff=0.5)
