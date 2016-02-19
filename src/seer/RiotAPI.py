
import requests
import Summoner

class RiotAPI(object):
    """Allows for querying and receiving data from the Riot Games Developer API
    
    Attributes:
        region_...: A string representing a League of Legends game region
        platform_...: A string representing a League of Legends platform
        
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
    region_BR = "br"
    region_EUNE = "eune"
    region_EUW = "euw"
    region_KR = "kr"
    region_LAN = "lan"
    region_LAS = "las"
    region_NA = "na"
    region_OCE = "oce"
    region_RU = "ru"
    region_TR = "tr"
    
    # Platform constants
    platform_BR1 = "BR1"
    platform_EUN1 = "EUN1"
    platform_EUW1 = "EUW1"
    platform_KR = "KR"
    platform_LA1 = "LA1"
    platform_LA2 = "LA2"
    platform_NA1 = "NA1"
    platform_OC1 = "OC1"
    platform_RU = "RU"
    platform_TR1 = "TR1"

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
        self.summoners = []
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
        if region == self.region_BR:
            return RiotAPI.platform_BR1
        elif region == self.region_EUNE:
            return RiotAPI.platform_EUN1
        elif region == self.region_EUW:
            return RiotAPI.platform_EUW1
        elif region == self.region_KR:
            return RiotAPI.platform_KR
        elif region == self.region_LAN:
            return RiotAPI.platform_LA1
        elif region == self.region_LAS:
            return RiotAPI.platform_LA2
        elif region == self.region_NA:
            return RiotAPI.platform_NA1
        elif region == self.region_OCE:
            return RiotAPI.platform_OC1
        elif region == self.region_RU:
            return RiotAPI.platform_RU
        elif region == self.region_TR:
            return RiotAPI.platform_TR1
        else:
            return False
    
    def lookup_summoner(self, name):
        """Gets all data associated with a summoner
        
        [long, detailed description here]
        
        Args:
            name: A string representing the summoner's name
        
        Returns:
            A dict containing all summoner data
        """
        name = name.lower().replace(" ", "")
        data = self.get("/api/lol/" + self.region 
                                            + "/v1.4/summoner/by-name/" + name)
        # Add basic summoner data to object
        summoner = Summoner.Summoner(data[name]['id'], data[name]['name'], 
                data[name]['profileIconId'], data[name]['revisionDate'], 
                data[name]['summonerLevel'])
        # Add ranked play data to object
        summoner.stats = self.get("/api/lol/" + self.region + 
                            "/v1.3/stats/by-summoner/" + str(summoner.id) + 
                            "/summary")['playerStatSummaries']
        self.summoners.append(summoner)
        return summoner

    def get(self, command):
        """Executes a GET command to the API
        
        Attempts to query the Riot Developer API via a REST GET command with
        the given url as the specific query and our already set api_key.
        
        Prints an error if the request returns anything other than HTTP 200 OK
        
        Args:
            command: A string containing the REST GET url to query
            
        Returns:
            The JSON response of the REST GET request
        """
        r = requests.get(self.url + command + "?api_key=" + self.api_key)
        if r.status_code != requests.codes.ok:
            print("HTTP ERROR: " + r.status_code + " " + r.reason)
        return r.json()