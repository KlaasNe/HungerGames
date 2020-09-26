from HelpFunctions import add_escapes


class Player:

    def __init__(self, name, gender, team_name, max_health=120, health=100, max_energy=100, energy=100):
        self.name = name
        self.esc_name = add_escapes(name)
        self.gender = gender
        self.team_name = team_name
        self.max_health = max_health
        self.health = health
        self.max_energy = max_energy
        self.energy = energy

        self.asleep = False
        self.kills = 0
        self.items = []

        pronouns = {"m": ["his", "him", "he"], "f": ["her", "her", "she"], "x": ["their", "them", "they"]}
        if self.gender.lower() not in pronouns.keys():
            self.gender = "x"
        self.pron1, self.pron2, self.pron3 = pronouns[self.gender.lower()]

    def is_dead(self):
        return self.health <= 0

    def to_string(self):
        return self.name

    def to_esc_string(self):
        return self.esc_name

    def to_info(self):
        return [self.name, self.health, self.energy, self.kills]
