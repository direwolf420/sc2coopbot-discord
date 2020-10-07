import sys
import os
import math
import random
from dotenv import load_dotenv

from core.custombot import CustomBot

load_dotenv()

# reads the .env file
# __debug__: This constant is true if Python was not started with an -O interpreter option
if __debug__:
    TOKEN = os.getenv("DISCORD_TOKEN")
    print("no debug")
else:
    TOKEN = os.getenv("DISCORD_TOKEN_DEBUG")
    print("debug")

version = 1

bot = CustomBot(__debug__)

bot.run(TOKEN)
