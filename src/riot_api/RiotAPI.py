
import requests

class RiotAPI(object):
    """Allows for querying and receiving data from the Riot Games Developer API
    
    See https://developer.riotgames.com/api/methods for a full API
    reference.
    
    Attributes:
        REGION_...: A string representing a League of Legends game region
        PLATFORM_...: A string representing a League of Legends platform
        
        The regions and platforms are:
            BR      (BR1)   Brazil
            EUNE    (EUN1)  Europe Nordic
            EUW     (EUW1)  Europe West
            KR      (KR)    Korea
            LAN     (LA1)   Latin America North
            LAS     (LA2)   Latin America South
            NA      (NA1)   North America
            OCE     (OC1)   Oceania
            RU      (RU)    Russia
            TR      (TR1)   Turkey
    """
    
    # Region constants
    REGION_BR = "br"
    REGION_EUNE = "eune"
    REGION_EUW = "euw"
    REGION_KR = "kr"
    REGION_LAN = "lan"
    REGION_LAS = "las"
    REGION_NA = "na"
    REGION_OCE = "oce"
    REGION_RU = "ru"
    REGION_TR = "tr"
    
    # Platform constants
    PLATFORM_BR1 = "BR1"
    PLATFORM_EUN1 = "EUN1"
    PLATFORM_EUW1 = "EUW1"
    PLATFORM_KR = "KR"
    PLATFORM_LA1 = "LA1"
    PLATFORM_LA2 = "LA2"
    PLATFORM_NA1 = "NA1"
    PLATFORM_OC1 = "OC1"
    PLATFORM_RU = "RU"
    PLATFORM_TR1 = "TR1"
    
    # Queue type constants
    ARAM = 'AramUnranked5x5'
    NORMAL_5V5 = 'Unranked'
    NORMAL_3V3 = 'Unranked3x3'
    RANKED_5V5_DYNAMIC = 'RankedSolo5x5'

    def __init__(self, api_key, region, url="https://na.api.pvp.net"):
        """Inits a new RiotAPI object with the given values
        
        A single RiotAPI object may only be valid for one region, and may 
        only use a single Riot Games Developer API key.
        
        Args:
            api_key: A string with the Riot Games Developer API key to use
                in queries.
            region: A string representing the region we want data from.
                Should be one of the region constants.
            url: The URL of the Riot Games Developer API to make REST
                requests to. Default value should probably not be changed.
        """
        self.api_key = api_key
        self.region = region
        self.url = url
        self.platform = self.determine_platform(region)
        
    def determine_platform(self, region):
        """Determines the server platform from the given region
        
        Takes the given region string and attempts to match it to a known
        server platform to allow API requests to that platform, when needed.
        
        Args:
            region: A string representing the region constant (see region
                constants).
        
        Returns:
            A string representing the platform constant for the given region.
            Returns False if the region is not defined
        """
        if region == self.REGION_BR:
            return RiotAPI.PLATFORM_BR1
        elif region == self.REGION_EUNE:
            return RiotAPI.PLATFORM_EUN1
        elif region == self.REGION_EUW:
            return RiotAPI.PLATFORM_EUW1
        elif region == self.REGION_KR:
            return RiotAPI.PLATFORM_KR
        elif region == self.REGION_LAN:
            return RiotAPI.PLATFORM_LA1
        elif region == self.REGION_LAS:
            return RiotAPI.PLATFORM_LA2
        elif region == self.REGION_NA:
            return RiotAPI.PLATFORM_NA1
        elif region == self.REGION_OCE:
            return RiotAPI.PLATFORM_OC1
        elif region == self.REGION_RU:
            return RiotAPI.PLATFORM_RU
        elif region == self.REGION_TR:
            return RiotAPI.PLATFORM_TR1
        else:
            return False
        
    def get_champions(self, free_to_play=False):
        """Gets status of all champions
        
        Returns the status of every champion by champion ID.
        See https://developer.riotgames.com/api/methods#!/1059/3658 for
        a full reference.
        
        Args:
            free_to_play: Only retrieves free-to-play champions if true.
            
        Returns:
            Dict containing all champion status data
        """
        args = {}
        if free_to_play:
            args = {"freeToPlay": True}
        query = "/api/lol/%s/v1.2/champion" % self.region
        return self.get(query, args)
    
    def get_champion_by_id(self, id):
        """Gets the status of a single champion by champion ID
        
        See https://developer.riotgames.com/api/methods#!/1059/3657 for
        a full reference.
        
        Args:
            id: the ID of the champion to retrieve data for
            
        Returns:
            Dict containing status data for the champion specified
        """
        query = "/api/lol/%s/v1.2/champion/%d" % self.region, id
        return self.get(query)
    
    def get_static_champion(self, id, additional_data="all"):
        """Gets static champion information by champion ID
        
        Returns a large amount of static champion data for the specified
        champion, such as hp, hpperlevel, name, description, etc.
        
        Args:
            id: the ID of the champion to retrieve static data from
        
        Returns:
            Dict containing static champion statistics for the specified
            champion
        """
        query = "/api/lol/static-data/%s/v1.2/champion/%d" % (self.region, id)
        args = {"champData" : additional_data}
        return self.get(query, args)
    
    def get_champ_mastery(self, player_id, champion_id):
        """Gets the champion mastery score for the specified player on the
        specified champion.
        
        See https://developer.riotgames.com/api/methods#!/1071/3697 for
        a full reference.
        
        Args:
            player_id: The unique summoner ID of the player
            champion_id: The champion ID of the player to get mastery for
        
        Returns:
            Dict containing various champion mastery statistics for the
            player/champion combination
        """
        query = "/championmastery/location/%s/player/%d/champion/%d" %\
                self.determine_platform(self.region), player_id, champion_id
        return self.get(query)
    
    def get_summoner_stats_summary(self, summoner_id):
        """Gets the stats summary for a summoner for all queues
        
        """
        query = "/api/lol/%s/v1.3/stats/by-summoner/%d/summary" %\
                (self.region, summoner_id)
        return self.get(query)
    
    def get_summoner_queue_summary(self, summoner_id, queue_type):
        """
        """
        summary = self.get_summoner_stats_summary(summoner_id)
        queues = len(summary['playerStatSummaries'])
        for i in range(0, queues):
            if summary['playerStatSummaries'][i]['playerStatSummaryType'] == queue_type:
                return summary['playerStatSummaries'][i]
        return False
    
    def get_summoner_by_name(self, name):
        """Gets basic data associated with a summoner or summoners
        
        Retrieves the basic metadata for a summoner (player) account.
        See https://developer.riotgames.com/api/methods#!/1061/3663 for
        a full reference.
        
        Args:
            name: A string representing the summoner's name or 
        
        Returns:
            A dict containing all summoner data
        """
        name = name.lower().replace(" ", "")
        return self.get("/api/lol/" + self.region + 
                        "/v1.4/summoner/by-name/" + name)
                        
    def get_summoner_id(self, name):
        """Returns a summoner's ID
        
        Returns the summoner ID corresponding to the specified summoner name
        
        Args:
            name: Summoner's name
            
        Returns:
            The summoner's ID
        
        """
        summoner = self.get_summoner_by_name(name)
        return summoner[name.lower()]["id"]

    def get(self, command, args={}):
        """Executes a GET command to the API
        
        Attempts to query the Riot Developer API via a REST GET command with
        the given url as the specific query and our already set api_key.
        
        Prints an error if the request returns anything other than HTTP 200 OK
        
        Args:
            command: A string containing the REST GET url to query
            
        Returns:
            The JSON response of the REST GET request
        """
        args["api_key"] = self.api_key
        r = requests.get(self.url + command, params=args)
        if r.status_code != requests.codes.ok:
            print("HTTP ERROR: %d %s" % (r.status_code, r.reason))
        return r.json()
