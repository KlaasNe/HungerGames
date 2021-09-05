from random import randint

import Items
from HelpFunctions import add_escapes


class Player:

    def __init__(self, name, gender, team_name, victory_msg="", max_health=120, health=100, max_energy=120, energy=100):
        self.name = name
        self.esc_name = add_escapes(name)
        self.gender = gender
        self.team_name = team_name
        self.victory_msg = victory_msg
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

    def get_dmg(self):
        dmg = 0
        for item in self.items:
            dmg += item.dmg
        return dmg

    def get_res(self):
        res = 0
        for item in self.items:
            res += item.res
        return res

    def get_prc(self):
        prc = 0
        for item in self.items:
            prc += item.prc
        return prc

    def get_weapon(self):
        weapons = []
        for item in self.items:
            if item.item_type == "weapon":
                weapons.append(item)
        return weapons

    def has_weapon(self):
        return True if self.get_weapon() else False

    def is_dead(self):
        return self.health <= 0

    def to_string(self):
        return self.name

    def to_esc_str(self):
        return self.esc_name

    def to_info(self):
        return [self.name, self.health, self.energy, self.kills]

    def give_weapon(self):
        item_nr = randint(0, len(Items.weapons["melee"]) - 1)
        item = Items.weapons["melee"][item_nr]
        if len(self.items) == 0:
            self.items.append(item)
        else:
            self.items[0] = item

    def take_dmg(self, dmg):
        self.health += dmg
        self.no_hp_overflow()

    def take_attack(self, dmg):
        hp_delta = -dmg - self.get_res() if self.get_res() > 0 else -dmg
        if hp_delta < 0:
            self.health += hp_delta

    def no_hp_overflow(self):
        if self.health > self.max_health:
            self.health = self.max_health
