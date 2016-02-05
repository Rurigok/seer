
class Summoner(object):
    
    def __init__(self, id, name, icon, revision, level):
        # Populate basic data
        self.id = id
        self.name = name
        self.icon = icon
        self.revision = revision
        self.level = level
        # Create empty lists
        self.stats = []
        self.queues = []
        self.matches = []
        
    def get_stats_by_queue(self, queue_type):
        pass