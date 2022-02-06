class Team:
    def __init__(self, name, vmsg=''):
        self.name = name
        self.victory_msg = name if vmsg == '' else vmsg
        self.players = set()
        self.allies = set()

    def get_name(self):
        return self.name

    def add_player(self, player):
        self.players.add(player)

    def get_alive(self):
        alive = []
        for player in self.players:
            if player.health > 0:
                alive.append(player)
        return alive

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

    def has_ally(self, team):
        return team in self.allies

    def size(self):
        return len(self.players)

    def size_alive(self):
        i = 0
        for player in self.players:
            if player.health > 0:
                i += 1
        return i

    def __eq__(self, other):
        return self.get_name() == other.get_name()

    def __hash__(self):
        return hash(self.name)
