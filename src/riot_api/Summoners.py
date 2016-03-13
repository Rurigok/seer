from riot_api import RiotAPI

"""
Helper methods for getting helpful statistics from the API easily
"""
    
def get_ranked_wl_ratio(api, summoner_name):
    """
    Gets the win/loss ratio of a summoner in ranked dynamic queue
    
    Args:
        summoner_name: The name of the summoner
        
    Returns:
        Win/loss ratio of the summoner in ranked queues
    """
    
    if not isinstance(api, RiotAPI):
        raise TypeError('api must be of type RiotAPI')
    
    if not type(summoner_name) is str:
        raise TypeError('summoner_name must be a string')

    stats = api.get_summoner_queue_summary(api.get_summoner_id(summoner_name), RiotAPI.RANKED_5V5_DYNAMIC)
    
    if not stats:
        return -1
    
    wins = stats['wins']
    losses = stats['losses']
    return float(wins) / float(losses)

class Summoner(object):
    """ The Summoner class represents a
    """
    
    def __init__(self, api, summoner_name):
        """ Builds a new Summoner object with summoner information
        """
        
        if not isinstance(api, RiotAPI):
            raise TypeError('api must be of type RiotAPI')
        
        if not type(summoner_name) is str:
            raise TypeError('summoner_name must be a string')
        
        self.name = summoner_name
        self.modified_name = summoner_name.replace(' ', '').lower()
        
        data = api.get_summoner_by_name(summoner_name)
        
        data = data[self.modified_name]
        
        self.id = int(data['id'])
        self.profileIconId = int(data['profileIconId'])
        self.revisionDate = int(data['revisionDate'])
        self.summonerLevel = int(data['summonerLevel'])

class SummonerStats(object):
    
    def __init__(self, summoner_name):
        pass