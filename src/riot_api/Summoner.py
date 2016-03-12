
from riot_api import RiotAPI

"""
Helper methods for getting helpful statistics from the API easily
"""
    
def get_ranked_wl_ratio(api, summoner_name):
    """
    Gets the win/loss ratio of a summoner in a specific queue type
    
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

