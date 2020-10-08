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

from discord.ext.commands import Bot, Cog, Context, Command
from discord.embeds import Embed
from discord.colour import Colour

class CommanderCog(Cog):
    pass