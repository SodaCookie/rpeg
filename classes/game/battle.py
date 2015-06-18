class Battle(object):

    def __init__(self, party, monsters):
        self.party = party
        self.players = self.party.players
        self.monsters = monsters