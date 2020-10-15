import sys
import os
import json
import re

from dotenv import load_dotenv

from core.custombot import CustomBot

load_dotenv()

release = "-r" in sys.argv # for testing purposes. When running the bot properly: `python bot.py -r`

# reads the .env file
if release:
    TOKEN = os.getenv("DISCORD_TOKEN")
    print("release")
else:
    TOKEN = os.getenv("DISCORD_TOKEN_DEBUG")
    print("debug")

version = 1

bot = CustomBot(release)

bot.run(TOKEN)
