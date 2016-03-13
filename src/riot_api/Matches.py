from riot_api import RiotAPI

"""
Helper methods for getting match statistics from the API easily
"""

def get_matches(api, summoner_name):
    
    if not isinstance(api, RiotAPI):
        raise TypeError('api must be of type RiotAPI')
    
    if not type(summoner_name) is str:
        raise TypeError('summoner_name must be a string')

    matches = api.get_match_list(api.get_summoner_id(summoner_name))
    
    return matches

class Match(object):
    """ The Match class represents a past match that a Summoner has played
    """
    def __init__(self, data):
        """ Builds a new match object from JSON data
        """
        
        # TODO build match object from JSON
        
        return
    
    @classmethod
    def from_match_id(cls, match_id):
        """ Builds a match object from the specified match id
        
        """
        if not type(match_id) is int:
            raise TypeError('match_id must be an int')
        
        # TODO get match data by match ID
        
        return cls(data)