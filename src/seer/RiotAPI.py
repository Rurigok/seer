
import requests
import Summoner

class RiotAPI(object):
    
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

    def __init__(self, api_key, region, url = "https://na.api.pvp.net"):
        self.api_key = api_key
        self.region = region
        self.url = url
        self.summoners = []
        self.platform = self.determine_platform(region)
        
    def determine_platform(self, region):
        if (region == "br"):
            return RiotAPI.platform_BR1
        elif (region == "eune"):
            return RiotAPI.platform_EUN1
        elif (region == "euw"):
            return RiotAPI.platform_EUW1
        elif (region == "kr"):
            return RiotAPI.platform_KR
        elif (region == "lan"):
            return RiotAPI.platform_LA1
        elif (region == "las"):
            return RiotAPI.platform_LA2
        elif (region == "na"):
            return RiotAPI.platform_NA1
        elif (region == "oce"):
            return RiotAPI.platform_OC1
        elif (region == "ru"):
            return RiotAPI.platform_RU
        elif (region == "tr"):
            return RiotAPI.platform_TR1
    
    
    def lookup_summoner(self, name):
        """ Gets all data associated with a summoner """
        name = name.lower().replace(" ", "")
        data = self.get("/api/lol/" + self.region + "/v1.4/summoner/by-name/" + name)
        # Add basic summoner data to object
        summoner = Summoner.Summoner(data[name]['id'], data[name]['name'], data[name]['profileIconId'], data[name]['revisionDate'], data[name]['summonerLevel'])
        # Add ranked play data to object
        summoner.stats = self.get("/api/lol/" + self.region + "/v1.3/stats/by-summoner/" + str(summoner.id) + "/summary")['playerStatSummaries']
        self.summoners.append(summoner)
        return summoner

    def get(self, command):
        """ Executes a GET command to the API """
        r = requests.get(self.url + command + "?api_key=" + self.api_key)
        if (r.status_code != requests.codes.ok):
            print("HTTP ERROR: " + r.status_code + " " + r.reason)
        return r.json()