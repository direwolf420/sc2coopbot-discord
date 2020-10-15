import json
import re
import os

from abc import ABC, abstractmethod

from discord.colour import Colour

import core.consts as consts
from core.requests import RequestType

class Aliasable(ABC):

    @abstractmethod
    def __init__(self, name:str, display_name:str, aliases:list):
        self.name = name
        self.display_name = display_name

        # make sure it's a string list
        self.aliases = [str(x) for x in aliases]
        # add its name to aliases too
        self.aliases.append(self.name)
        
    # order matters here
    @staticmethod
    @abstractmethod
    def from_alias(alias:str):
        pass

    def __str__(self):
        return self.display_name

    def __repr__(self):
        return self.display_name

class Guide(Aliasable):

    def __init__(self, name:str, url_source:str, display_name:str, aliases:list):
        super().__init__(name, display_name, aliases)
        self._page_url = "{}/{}/{}".format(consts.SC2COOP_URL, url_source, self.name)

    def get_page(self):
        return self._page_url

    def from_alias(alias:str):
        """returns a Guide if it matches that alias, None if not found"""
        # that's how you access super from a static method
        super(Guide, Guide).from_alias(alias)
        for k,v in guidecache.items():
            if alias in v.aliases:
                return v
        return None

class Mutator(Aliasable):

    def __init__(self, name:str, display_name:str, aliases:list):
        super().__init__(name, display_name, aliases)
        self._page_url = "{}/resources/mutators#row_{}".format(consts.SC2COOP_URL, self.name)
        self._image_url = "{}/images/mutators/{}.png".format(consts.SC2COOP_URL, self.name)

    def get_page(self):
        return self._page_url

    def get_profile(self):
        return (self.display_name, self._image_url)

    def from_alias(alias:str):
        """returns a Mutator if it matches that alias, None if not found"""
        # TODO difflib stuff here cause no way im manually typing out all possible mutator aliases
        super(Mutator, Mutator).from_alias(alias)
        for k,v in mutatorcache.items():
            if alias in v.aliases:
                return v
        return None

class Commander(Aliasable):

    def __init__(self, name:str, display_name:str, aliases:list, colour:Colour):
        super().__init__(name, display_name, aliases)
        self._image_url = "{}/images/commanderportraits/{}portrait.png".format(consts.SC2COOP_URL, self.name)
        self._page_url = "{}/commanders/{}".format(consts.SC2COOP_URL, self.name)
        self._summary_url = "{}/images/endpoints/{}.png".format(consts.SC2COOP_URL, self.name)

        self.colour = colour

    def get_profile(self):
        return (self.display_name, self._image_url)

    def get_summary(self):
        return self._summary_url

    def get_page(self, requestType:RequestType):
        anchor = requestType.get_anchor()
        url = self._page_url
        if anchor is not None:
            return "{0}#{1}".format(url, anchor)
        return self._page_url

    def from_alias(alias:str):
        """returns a Commander if it matches that alias, None if not found"""
        # that's how you access super from a static method
        super(Commander, Commander).from_alias(alias)
        for k,v in commandercache.items():
            if alias in v.aliases:
                return v
        return None

class Map(Aliasable):

    def __init__(self, name:str, display_name:str, aliases:list, common_alias:str):
        super().__init__(name, display_name, aliases)
        self._page_url = "{}/missions/{}".format(consts.SC2COOP_URL, self.name)
        self.common_alias = common_alias
        self.aliases.append(self.common_alias.lower())

    def get_page(self):
        return self._page_url

    def from_alias(alias:str):
        """returns a Map if it matches that alias, None if not found"""
        super(Map, Map).from_alias(alias)
        for k,v in mapcache.items():
            if alias in v.aliases:
                return v
        return None

def verify_duplicates(cache:dict):
    uniques = set()

    for v in cache.values():
        if not isinstance(v, Aliasable):
            # to make sure we can use the aliases field
            raise Exception("{} is not  of type 'Aliasable'".format(v))

        for alias in v.aliases:
            if alias not in uniques:
                uniques.add(alias)
            else:
                raise Exception("Duplicate name '{0}' found in '{1}'".format(alias, v))

    return True

def display_name_to_internal_name(display_name:str):
    """
    Sanitizes a display name (that can contain spaces or special characters)
    'Afraid of the Dark' -> 'afraidofthedark'
    """
    split = re.split("[^0-9a-zA-Z]+", display_name)
    name = str()
    for s in split:
        name += s.lower()
    return name

commandercache = dict()

commandercache[consts.RAYNOR] = Commander(consts.RAYNOR, "Raynor", ["ray", "cowboy", "hotshot", "jim", "jimmy", "chief"], Colour(0x0042ff))
commandercache[consts.KERRIGAN] = Commander(consts.KERRIGAN, "Kerrigan", ["kerri", "sarah", "queen"], Colour(0xff00ff))
commandercache[consts.ARTANIS] = Commander(consts.ARTANIS, "Artanis", ["arti", "arty", "sinatra", "skippy"], Colour(0x1ca7ea))
commandercache[consts.SWANN] = Commander(consts.SWANN, "Swann", ["rory"], Colour(0xfe8a0e))
commandercache[consts.ZAGARA] = Commander(consts.ZAGARA, "Zagara", ["zag", "zergy", "overqueen", "broodmother"], Colour(0x3300bf))
commandercache[consts.VORAZUN] = Commander(consts.VORAZUN, "Vorazun", ["vora", "matriarch"], Colour(0x540081))
commandercache[consts.KARAX] = Commander(consts.KARAX, "Karax", ["cannonrusher", "phasesmith", "phase-smith"], Colour(0xebe129))
commandercache[consts.ABATHUR] = Commander(consts.ABATHUR, "Abathur", ["aba", "slug"], Colour(0xebe129))
commandercache[consts.ALARAK] = Commander(consts.ALARAK, "Alarak", ["ala", "highlord"], Colour(0x400000))
commandercache[consts.NOVA] = Commander(consts.NOVA, "Nova", ["ace", "ass", "november", "terra", "annabella"], Colour(0x1ca7ea))
commandercache[consts.STUKOV] = Commander(consts.STUKOV, "Stukov", ["stuk", "stucco"], Colour(0xcca6fc))
commandercache[consts.FENIX] = Commander(consts.FENIX, "Fenix", ["talandar", "purifier"], Colour(0xfe8a0e))
commandercache[consts.DEHAKA] = Commander(consts.DEHAKA, "Dehaka", ["haka", "rockslapper", "rockslap", "rock", "catsicle", "cat"], Colour(0x69c7d6))
commandercache[consts.HORNER] = Commander(consts.HORNER, "Han & Horner", ["han", "hanhorner", "hanandhorner", "han&horner", "hnh", "hh", "h&h", "mira", "matt"], Colour(0x4a1b47))
commandercache[consts.TYCHUS] = Commander(consts.TYCHUS, "Tychus", ["tych", "findlay"], Colour(0xa76942))
commandercache[consts.ZERATUL] = Commander(consts.ZERATUL, "Zeratul", ["zera", "tool", "zeratool", "prelate", "zeracool"], Colour(0x00a762))
commandercache[consts.STETMANN] = Commander(consts.STETMANN, "Stetmann", ["egon", "stet", "stetman", "lagman", "lagmann", "stetboi", "scientist"], Colour(0xfe8a0e))
commandercache[consts.MENGSK] = Commander(consts.MENGSK, "Mengsk", ["arcturus", "emperor"], Colour(0x661f1f))

assert commandercache.__len__() == consts.COMM_COUNT
assert verify_duplicates(commandercache)

mapcache = dict()

mapcache[consts.COA] = Map(consts.COA, "Chain of Ascension", ["chain", "ascension"], "CoA")
mapcache[consts.COD] = Map(consts.COD, "Cradle of Death", ["cradle", "death", "tomato", "tomatofarm", "farm", "cok", "truck"], "CoD")
mapcache[consts.DON] = Map(consts.DON, "Dead of Night", ["dead", "night"], "DoN")
mapcache[consts.LNL] = Map(consts.LNL, "Lock and Load", ["lockandload", "lock", "l&l", "ll"], "LnL")
mapcache[consts.MW] = Map(consts.MW, "Malwarfare", ["mal", "warfare"], "MW")
mapcache[consts.ME] = Map(consts.ME, "Miner Evacuation", ["miner", "evacuation"], "ME")
mapcache[consts.MO] = Map(consts.MO, "Mist Opportunities", ["mist", "opportunities"], "MO")
mapcache[consts.OE] = Map(consts.OE, "Oblivion Express", ["oblivion", "express", "orgo"], "OE")
mapcache[consts.PNP] = Map(consts.PNP, "Part and Parcel", ["partandparcel", "part", "parcel", "p&p", "pp", "cancer"], "PnP")
mapcache[consts.RTK] = Map(consts.RTK, "Rifts to Korhal", ["rifts", "korhal"], "RtK")
mapcache[consts.SOA] = Map(consts.SOA, "Scythe of Amon", ["scythe", "amon"], "SoA")
mapcache[consts.TOTP] = Map(consts.TOTP, "Temple of the Past", ["temple", "past"], "TotP")
mapcache[consts.VP] = Map(consts.VP, "Vermillion Problem", ["vermillion", "problem"], "VP")
mapcache[consts.VL] = Map(consts.VL, "Void Launch", ["launch"], "VL")
mapcache[consts.VT] = Map(consts.VT, "Void Thrashing", ["void", "thrash", "thrashing", "trashing", "hammer"], "VT")

assert mapcache.__len__() == consts.MAP_COUNT
assert verify_duplicates(mapcache)

guidecache = dict()

source = "guides"
guidecache[consts.BUILD_ORDER] = Guide(consts.BUILD_ORDER, source, "Build Order Theory", ["bo", "build", "order"])
guidecache[consts.ENEMY_COMPS] = Guide(consts.ENEMY_COMPS, source, "Enemy Compositions", ["enemy", "amon", "attack", "wave", "waves", "comp", "comps", "compositions"])
guidecache[consts.GENERAL_TIPS] = Guide(consts.GENERAL_TIPS, source, "General Tips", ["general", "tips", "tricks", "advice", "help"])
guidecache[consts.NEW_PLAYERS] = Guide(consts.NEW_PLAYERS, source, "New Players", ["new", "players", "noobs", "commander", "selection"])

source = "resources"
guidecache[consts.ACHIEVEMENTS] = Guide(consts.ACHIEVEMENTS, source, "Achievements", ["ach", "cheevos"])
guidecache[consts.AI_LOGIC] = Guide(consts.AI_LOGIC, source, "AI Logic", ["ai", "logic"])
guidecache[consts.BRUTAL_PLUS] = Guide(consts.BRUTAL_PLUS, source, "Brutal+", ["brutal+", "plus", "brutalplus"])
guidecache[consts.DEATH_PREVENTION] = Guide(consts.DEATH_PREVENTION, source, "Death Prevention Effects", ["death", "prevention"])
guidecache[consts.EASTER_EGGS] = Guide(consts.EASTER_EGGS, source, "Easter Eggs", ["easter", "eggs"])
guidecache[consts.LEVELS] = Guide(consts.LEVELS, source, "Levels, Masteries, Ascension", ["experience", "exp", "mastery", "masteries", "ascension"])
guidecache[consts.PATCHDATA] = Guide(consts.PATCHDATA, source, "Patchnotes", ["patch"])
guidecache[consts.STATS] = Guide(consts.STATS, source, "SC2Coop Stats", [])
guidecache[consts.WEEKLYMUTATIONS] = Guide(consts.WEEKLYMUTATIONS, source, "Weeky Mutations", ["weekly", "mutation", "mutations"])

assert guidecache.__len__() == consts.GUIDE_COUNT
assert verify_duplicates(guidecache)

file = "mutators.json"
if not os.path.exists(file):
    orig = "Afraid of the Dark - Aggressive Deployment - Alien Incubation - Avenger - Barrier - Black Death - Blizzard - Boom Bots - Chaos Studios - Concussive Attacks - Darkness - Diffusion - Double Edged - Eminent Domain - Evasive Maneuvers - Fatal Attraction - Fear - Fireworks - Gift Exchange - Going Nuclear - Hardened Will - Heroes From the Storm - Inspiration - Just Die - Kill Bots - Laser Drill - Lava Burst - Life Leech - Long Range - Lucky Envelopes - Mag-nificent - Micro Transactions - Mineral Shields - Minesweeper - Missile Command - Moment of Silence - Mutually Assured Destruction - Naughty List - Orbital Strike - Outbreak - Photon Overload - Polarity - Power Overwhelming - Propagators - Purifier Beam - Random - Scorched Earth - Self Destruction - Sharing is Caring - Shortsighted - Slim Pickings - Speed Freaks - Temporal Field - Time Warp - Transmutation - Trick or Treat - Turkey Shoot - Twister - Vertigo - Void Reanimators - Void Rifts - Walking Infested - We Move Unseen"
    split = orig.split(" - ")
    data = list()
    for display_name in split:
        name = display_name_to_internal_name(display_name)
        data.append({"name":name, "display_name":display_name})

    with open(file, "w+") as handle:
        handle.write(json.dumps(data, sort_keys=True, indent=4))

if not os.path.exists(file):
    raise Exception("Failed to find '{}'".format(file))

mutatorcache = dict()

with open(file) as handle:
    mutatordata = json.load(handle)

    if mutatordata.__len__() is 0:
        raise Exception("Invalid file '{}'".format(file))

    for m in mutatordata:
        name = m["name"]
        display_name = m["display_name"]
        mutatorcache[name] = Mutator(name, display_name, [])

