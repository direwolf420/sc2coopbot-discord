import ast
import math
import sys
import re

import urllib.parse
import urllib.request

import core.utils as ut

#import aiohttp

import core.consts as consts
import core.caches as cc

from core.caches import Commander, Map
from core.field import Field
from core.requests import RequestHandler, RequestType

from discord.ext.commands import Bot
from discord.ext.commands import Context
from discord.ext.commands import Command
from discord.embeds import Embed
from discord.colour import Colour

class BotCommands():

    def __init__(self, bot:Bot):
        self.bot = bot
        self.request_handler = RequestHandler()

    #bot.add_command(Command(adsadsads, name="asd", description="tests", aliases=["a"]))

    #@bot.command(name="trivia", description="Get a random fact about SC2 Coop", aliases=["ray"])
    async def trivia(self, ctx:Context):
        if ut.early_return(self.bot, ctx):
            return

        trivias = list()
        trivias.append("Dehakas 'Broodbrother' prestige is a jab at the easter egg with his missing arm found in the campaign mission 'Supreme'")
    
        await self.bot.sendf(ctx, random.choice(trivias),
                        author=("Trivia!", "https://starcraft2coop.com/images/commanderportraits/dehakaportrait.png",),
                        colour=Colour.green(), footer=True)


    async def testcommand(self, ctx:Context):
        if ut.early_return(self.bot, ctx):
            return
        a = "Raynor trains combat units and builds Barracks 50% faster.\r\nMechanical units cost 20% less gas.\r\nStimpack grants increase bonuses, costs less life, and does not require research.";
        
        await self.bot.sendf(ctx, a)

    async def help_wrapper(self, ctx):
        """References the doc"""
        prefix = ctx.prefix
        await self.bot.sendf(ctx, title="Use `{0}help {1}`".format(prefix, ctx.invoked_with))

    def get_last_number(self, s:str):
        """Returns the last integer found in a string (-1 if none)"""
        array = re.findall(r'[0-9]+', s)
        if array.__len__() is 0:
            return -1
        return int(array[-1])

    async def commander_cmd(self, ctx:Context, *args):
        """
        Fetches info about a commander

        Possible args:
        * h | help
        -> Tells you to use the help command

        * commanderalias
        -> Gives introduction to the given commander

        The following args when prefixed with commanderalias:

        * [(level(s) | l(s) | unlock(s)] [number]) | l[number]
        -> List all level unlocks, or if a number is specified, the unlock description

        * [(master(y|ies) | m(s)] [number]) | m[number]
        -> List all masteries, or if a number is specified, the options

        * [(prestige(s) | p(s)] [number]) | p[number]
        -> List all prestiges, or if a number is specified, the (dis)advantages

        * unit(s) | u(s)
        -> List all units

        Basic usage:
        >>> [prefix]c ray p2 -> Lists (dis)advantages of Raynors second prestige
        """

        if ut.early_return(self.bot, ctx):
            return
        
        count = args.__len__()
        sargs = [a.lower() for a in args] # sanitize to lowercase only
        if count == 0:
            await self.help_wrapper(ctx)
            return

        alias = sargs[0]

        if alias in ("h", "help"):
            await self.help_wrapper(ctx)
            return

        comm = Commander.from_alias(alias)
        queryType = RequestType.NONE

        if comm is None:
            await self.bot.sendf(ctx, title=consts.ERR_STR, description="No commander with alias '{}' found!".format(alias))
            # todo give back list of possible operations
            return

        if count == 1:
            fields = (Field("More Info", comm.get_page(queryType)),)
            await self.bot.sendf(ctx, fields=fields, author=comm.get_profile(), colour=comm.colour, image_url=comm.get_summary(), footer=True)
            return

        query = {"commander":comm.name}

        if count >= 2:
            operation = sargs[1]

            l_prefixes = RequestType.EXACTLEVEL.get_aliases("l") + RequestType.EXACTLEVEL.get_aliases("level") + RequestType.EXACTLEVEL.get_aliases("unlock")
            m_prefixes = RequestType.EXACTMASTERY.get_aliases("m") + RequestType.EXACTMASTERY.get_aliases("mastery")
            p_prefixes = RequestType.EXACTPRESTIGE.get_aliases("p") + RequestType.EXACTPRESTIGE.get_aliases("prestige")

            # no "u or us" because thats for units
            if operation in set(("l", "ls", "level", "levels", "unlock", "unlocks") + l_prefixes):
                query["type"] = "unlock"
                queryType = RequestType.LISTLEVELS
                
                level_str = str()

                if count == 2 and operation in l_prefixes:
                    level_str = operation
                
                if count >= 3:
                    level_str = sargs[2]

                level = ut.get_last_number(level_str) # take last number of the string
                
                if level in RequestType.EXACTLEVEL.get_range():
                    query["level"] = level
                    queryType = RequestType.EXACTLEVEL

            elif operation in set(("m", "ms", "mastery", "masteries") + m_prefixes):
                query["type"] = "mastery"
                queryType = RequestType.LISTMASTERIES

                level_str = str()

                if count == 2 and operation in m_prefixes:
                    level_str = operation

                if count >= 3:
                    level_str = sargs[2]

                level = ut.get_last_number(level_str) # take last number of the string

                if level in RequestType.EXACTMASTERY.get_range():
                    query["level"] = level
                    queryType = RequestType.EXACTMASTERY

            elif operation in set(("p", "ps", "prestige", "prestiges") + p_prefixes):
                query["type"] = "prestige"
                queryType = RequestType.LISTPRESTIGES

                level_str = str()

                if count == 2 and operation in p_prefixes:
                    level_str = operation

                if count >= 3:
                    level = sargs[2]

                level = ut.get_last_number(level_str) # take last number of the string
                    
                if level in RequestType.EXACTPRESTIGE.get_range():
                    query["level"] = level
                    queryType = RequestType.EXACTPRESTIGE
                    
            elif operation in ("u", "us", "unit", "units"):
                query["type"] = "unit"
                queryType = RequestType.UNITS

            else:
                #await self.bot.sendf(ctx, title=consts.ERR_STR, description="Not a supported operation: {}".format(operation))
                return

        # if the code gets to here, we have a request to make

        params = urllib.parse.urlencode(query) # builds url params to append to the site
        (exception, data) = self.request_handler.get_data_from_site(params)

        if exception:
            error = "Exception occured with params {}".format(data["params"])
            if "misc" in data:
                if data["misc"] == consts.ERR_STR:
                    error += ": Invalid input"
            await self.bot.sendf(ctx, error, title=consts.ERR_STR, colour=Colour.red())

        else:
            description = None
            fields = ()
            send = False
            if queryType is RequestType.LISTLEVELS:
                #{"data":["Level 1: Mutating Carapace","Level 2: Immobilization Wave","Level 3: Ruthlessness","Level 4: Spawning Pool Upgrade Cache","Level 5: New Unit:Lurker","Level 6: Hydralisk & Lurker Upgrade Cache","Level 7: Malignant Creep","Level 8: Omega Worm","Level 9: Kerrigan Upgrade Cache","Level 10: Fury","Level 11: Spire Upgrade Cache","Level 12: Zergling Evolution: Raptor","Level 13: Ultralisk Upgrade Cache","Level 14: Ultralisk Evolution: Torrasque","Level 15: Queen of Blades"]}
                
                levels = data["data"]

                level_desc = str()
                lvl = 0
                for level in levels:
                    lvl += 1
                    level_desc += "\r\n{0}: {1}".format(lvl, level)

                fields = (Field("Leveling Unlocks", level_desc),)
                send = True

            elif queryType is RequestType.EXACTLEVEL:
                # {'name': 'Mercenary Munitions', 'description': "Increases the attack speed of Raynor's combat units and calldowns by 15%."}

                whichlevel = "Level {}: ".format(query["level"]) + data["name"];

                # .encode().decode('unicode_escape') formats the escape characters (\\ -> \)
                level_desc = data["description"].encode().decode('unicode_escape')
                fields = (Field(whichlevel, level_desc),)
                send = True
            
            elif queryType is RequestType.LISTMASTERIES:
                #{"data":{"1":["Research Resource Cost","Speed Increases for Drop Pod Units"],"2":["Hyperion Cooldown","Banshee Airstrike Cooldown"],"3":["Medics Heal Additional Target","Mech Attack Speed"]}}
                
                # =>
                # Set 1
                # • Research Resource Cost
                # • Speed Increases for Drop Pod Units
                # Set 2
                # etc

                mastery_sets = data["data"]
                description = "**Mastery Sets**"

                for k,v in mastery_sets.items():
                    combined_set = str()
                    for masteries in v:
                        combined_set += "\r\n• {}".format(masteries)
                    which_set = "Set {}".format(k)
                    fields = fields + (Field(which_set, combined_set),)
                send = True

            elif queryType is RequestType.EXACTMASTERY:
                # {"option1":{"power":"Hyperion Cooldown","value":"-4 sec per point, -120 sec maximum"},"option2":{"power":"Banshee Airstrike Cooldown","value":"-4 sec per point, -120 sec maximum"}}
                
                # =>
                # Set 2
                #
                # Option 1: Hyperion Cooldown
                # • -4 sec per point, -120 sec maximum
                #
                # Option 2: Banshee Airstrike Cooldown
                # • -4 sec per point, -120 sec maximum

                description = "**Mastery Set {}**".format(query["level"]);
                for k,v in data.items():
                    # v is a dict with "power" and "value" fields
                    which_option = "Option {}: ".format(k[-1])
                    fields = fields + (Field(which_option + v["power"], "• {}".format(v["value"])),)

                send = True
                
            elif queryType is RequestType.LISTPRESTIGES:
                #{"data":["Backwater Marshal","Rough Rider","Rebel Raider"]}
                
                # =>
                # Set 1
                # • Research Resource Cost
                # • Speed Increases for Drop Pod Units
                # Set 2
                # etc

                prestiges = data["data"]
                description = "**Prestiges**"
                
                lvl = 0
                for prestige in prestiges:
                    lvl += 1
                    prestige_name = "• {}".format(prestige)
                    which_prestige = "Prestige {}".format(lvl)
                    fields = fields + (Field(which_prestige, prestige_name),)
                send = True

            elif queryType is RequestType.EXACTPRESTIGE:
                # {"name":"Rebel Raider","description":{"advantages":"The Starport, Armory and Orbital Command no longer have tech requirements.\\r\\nThe Starport no longer has a gas cost and its units cost 30% less gas\\r\\nVikings, Banshees and Battlecruisers increase top bar cooldown rates by 1% per supply used.","disadvantages":"Combat units cost 50% more minerals."}}
                
                # =>
                # Prestige 1: Rebel Raider
                #
                # Advantages
                # • first
                # • second
                #
                # Disadvantages
                # • first
                # • second

                description = "**Prestige {0}: {1}**".format(query["level"], data["name"]);
                for k,v in data["description"].items():
                    # k is adv/disadv, v is the explanation 
                    adv_disadv = k.capitalize()
                    split = "\r\n"
                    desc_list = v.encode().decode('unicode_escape').split(split)
                    desc = str()
                    for subdesc in desc_list:
                        desc += "\r\n• {}".format(subdesc)
                    fields = fields + (Field(adv_disadv, desc),)

                send = True

            elif queryType is RequestType.UNITS:
                # {"data":"Marine, Firebat, Medic, Marauder, Vulture, Siege Tank, Viking, Banshee, Battlecruiser, Orbital Command Center, Bunker, Missile Turret"}

                title = "Units/Buildings";

                units = "```{}```".format(data["data"])
                fields = (Field(title, units),)
                send = True

            if send:
                if comm is not None:
                    fields = fields + (Field("More Info", comm.get_page(queryType)),)
                await self.bot.sendf(ctx, description=description, fields=fields, author=comm.get_profile(), colour=comm.colour, footer=True)
        
    async def map_cmd(self, ctx:Context, *args):
        """
        Fetches info about a map/mission

        Possible args:
        * none
        -> Lists all maps

        * mapalias
        -> Fetches info about this particular map (no spaces)

        Basic usage:
        >>> [prefix]m vt -> description of Void Thrashing
        """

        if ut.early_return(self.bot, ctx):
            return
        
        count = args.__len__()
        sargs = [a.lower() for a in args] # sanitize to lowercase only
        if count == 0:

            fields = ()
            all = "```"
            for v in cc.mapcache.values():
                # makes the left hand always have atleast four length, fills with " "
                all += "\r\n{m: <4}: {d}".format(m=v.common_alias, d=v.display_name)
            all += "```"

            fields = (Field("All Maps", all),)

            prefix = ctx.prefix
            example = "Use `{0}{1} vt` to get more info about Void Thrashing".format(prefix, ctx.command.name)

            fields = fields + (Field("Example", example),)

            await self.bot.sendf(ctx, fields=fields)

            return

        alias = sargs[0]

        if alias in ("h", "help"):
            await self.help_wrapper(ctx)
            return

        map = Map.from_alias(alias)

        if map is None:
            await self.bot.sendf(ctx, title=consts.ERR_STR, description="No map/mission with alias '{}' found!".format(alias))
            return

        query = {"mission":map.name}
        query["type"] = "mission"

        # if the code gets to here, we have a request to make

        params = urllib.parse.urlencode(query) # builds url params to append to the site
        (exception, data) = self.request_handler.get_data_from_site(params)

        if exception:
            error = "Exception occured with params {}".format(data["params"])
            if "misc" in data:
                if data["misc"] == consts.ERR_STR:
                    error += ": Invalid input"
            await self.bot.sendf(ctx, error, title=consts.ERR_STR, colour=Colour.red())

        else:
            # {"data":"Amon is using Kaldir's warp conduits to transport his troops across the sector. Destroy the shuttles carrying the troops before they reach the warp conduits."}
            send = False
            description = data["data"]

            title = "{0} (**{1}**)".format(map.display_name, map.common_alias)
            fields = (Field("Description", description),)
            fields = fields + (Field("More Info", map.get_page()),)

            await self.bot.sendf(ctx, title=title, fields=fields, footer=True)

        
    def add_commands(self):
        """
        todo:
        redirects to amon unit comps
        redirects to maguro stuff
        praise eddie
        """
        self.bot.add_command(Command(self.commander_cmd, name="c", aliases=["cmd", "comm", "commander"]))
        self.bot.add_command(Command(self.map_cmd, name="m", aliases=["map", "maps", "mission", "missions"]))
        #self.bot.add_command(Command(self.testcommand, name="asd", aliases=["a"]))
