class Team:
    def __init__(self, name):
        self.name = name
        self.players = set()
        self.allies = set()

    def get_name(self):
        return self.name

    def add_player(self, player):
        self.players.add(player)

    def remove_player(self, player):
        try:
            self.players.remove(player)
        except KeyError:
            pass

    def add_ally(self, team):
        self.allies.add(team)

    def remove_ally(self, team):
        try:
            self.allies.remove(team)
        except KeyError:
            pass

    def has_as_ally(self, team):
        return team in self.allies

    def size(self):
        return len(self.players)

    def __eq__(self, other):
        return self.get_name() == other.get_name()

    def __hash__(self):
        return hash(self.name)
