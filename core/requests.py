import ast
import sys

import urllib

from enum import Enum, auto
from discord.ext.commands import Bot
import core.consts as consts

class RequestHandler():

    def __init__(self):
        self.cache = dict()

    def get_data_from_site(self, query:dict):
        """Returns a tuple (bool, dict)"""

        params = urllib.parse.urlencode(query) # builds url params to append to the site

        if params in self.cache:
            return (False, self.cache[params])

        # If first element is True, it means there was some error. dict will be populated with a params key and a possible misc key
        try:
            url = "{0}/scripts/endpoints/discord.php?{1}".format(consts.SC2COOP_URL, params)

            #async with aiohttp.ClientSession() as session:
            #    async with session.get(url) as r:
            #        s = #idk
            #        data = ast.literal_eval(s)
            #        return (False, data)

            # blocking = bad
            with urllib.request.urlopen(url) as f:
                response = f.read()
                s = response.decode('utf-8')
                if s == consts.ERR_STR:
                    return (True, dict({"params":params, "misc":s}))
                data = ast.literal_eval(s)

                if params not in self.cache:
                    self.cache[params] = data

                return (False, data)
        except:
            print("ERROR:{}".format(str(sys.exc_info()[0]) + str(sys.exc_info()[1]) + str(sys.exc_info()[2])))
            return (True, dict({"params":params}))


class RequestType(Enum):

    NONE = auto()

    LISTLEVELS = auto()
    EXACTLEVEL = auto()

    LISTMASTERIES = auto()
    EXACTMASTERY = auto()

    LISTPRESTIGES = auto()
    EXACTPRESTIGE = auto()

    UNITS = auto()

    def get_range(self):
        if self in (self.LISTLEVELS, self.EXACTLEVEL):
            return range(1, 15 + 1)
        elif self in (self.LISTMASTERIES, self.EXACTMASTERY, self.LISTPRESTIGES, self.EXACTPRESTIGE):
            return range(1, 3 + 1)
        return range(1, 1)

    def get_aliases(self, prefix:str):
        """returns a tuple of strings"""
        aliases = ()
        for i in self.get_range():
            aliases = aliases + (prefix + str(i),)
        return aliases

    def get_anchor(self):
        if self in (self.LISTLEVELS, self.EXACTLEVEL):
            return "levelUnlocks"
        if self in (self.LISTMASTERIES, self.EXACTMASTERY):
            return "masteries"
        if self in (self.LISTPRESTIGES, self.EXACTPRESTIGE):
            return "prestiges"
        if self is self.UNITS:
            return "units"
        return None