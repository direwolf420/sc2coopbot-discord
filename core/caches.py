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
    checkedinstance = False
    
    uniques = set()

    for v in cache.values():
        if not checkedinstance:
            checkedinstance = True
            if not isinstance(v, Aliasable):
                # to make sure we can use the aliases field
                return False

        for alias in v.aliases:
            if alias not in uniques:
                uniques.add(alias)
            else:
                return False

    return True

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
commandercache[consts.DEHAKA] = Commander(consts.DEHAKA, "Dehaka", ["haka", "rockslapper"], Colour(0x69c7d6))
commandercache[consts.HORNER] = Commander(consts.HORNER, "Han & Horner", ["han", "hanhorner", "hanandhorner", "han&horner", "hnh", "hh", "h&h", "mira", "matt"], Colour(0x4a1b47))
commandercache[consts.TYCHUS] = Commander(consts.TYCHUS, "Tychus", ["tych", "findlay"], Colour(0xa76942))
commandercache[consts.ZERATUL] = Commander(consts.ZERATUL, "Zeratul", ["zera", "tool", "zeratool", "prelate"], Colour(0x00a762))
commandercache[consts.STETMANN] = Commander(consts.STETMANN, "Stetmann", ["egon", "stet", "stetman", "lagman", "lagmann", "stetboi", "scientist"], Colour(0xfe8a0e))
commandercache[consts.MENGSK] = Commander(consts.MENGSK, "Mengsk", ["arcturus", "emperor"], Colour(0x661f1f))

assert commandercache.__len__() == consts.COMM_COUNT
assert verify_duplicates(commandercache)

mapcache = dict()

mapcache[consts.COA] = Map(consts.COA, "Chain of Ascension", ["chain", "ascension"], "CoA")
mapcache[consts.COD] = Map(consts.COD, "Cradle of Death", ["cradle", "death"], "CoD")
mapcache[consts.DON] = Map(consts.DON, "Dead of Night", ["dead", "night"], "DoN")
mapcache[consts.LNL] = Map(consts.LNL, "Lock and Load", ["lockandload", "lock", "l&l", "ll"], "LnL")
mapcache[consts.MW] = Map(consts.MW, "Malwarfare", ["mal", "warfare"], "MW")
mapcache[consts.ME] = Map(consts.ME, "Miner Evacuation", ["miner", "evacuation"], "ME")
mapcache[consts.MO] = Map(consts.MO, "Mist Opportunities", ["mist", "opportunities"], "MO")
mapcache[consts.OE] = Map(consts.OE, "Oblivion Express", ["oblivion", "express", "orgo"], "OE")
mapcache[consts.PNP] = Map(consts.PNP, "Part and Parcel", ["ppartandparcel", "part", "parcel", "p&p", "pp"], "PnP")
mapcache[consts.RTK] = Map(consts.RTK, "Rifts to Korhal", ["rifts", "korhal"], "RtK")
mapcache[consts.SOA] = Map(consts.SOA, "Scythe of Amon", ["scythe", "amon"], "SoA")
mapcache[consts.TOTP] = Map(consts.TOTP, "Temple of the Past", ["temple", "past"], "TotP")
mapcache[consts.VP] = Map(consts.VP, "Vermillion Problem", ["vermillion", "problem"], "VP")
mapcache[consts.VL] = Map(consts.VL, "Void Launch", ["launch"], "VL")
mapcache[consts.VT] = Map(consts.VT, "Void Thrashing", ["void", "thrash", "thrashing", "trashing"], "VT")

assert mapcache.__len__() == consts.MAP_COUNT
assert verify_duplicates(mapcache)