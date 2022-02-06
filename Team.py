class Team:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.allies = []

    def get_name(self):
        return self.name

    def get_players(self):
        return self.players

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        self.players.remove(player)

    def get_allies(self):
        return self.allies

    def add_ally(self, team):
        self.allies.append(team)

    def remove_ally(self, team):
        self.allies.remove(team)

    def has_as_ally(self, team):
        return team in self.get_allies()

    def __eq__(self, other):
        return self.get_name() == other.get_name()
