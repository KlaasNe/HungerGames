from random import randint

from Singleton import Singleton


class Event:

    def __init__(self, description, hp_req=0, self_hp_delta=0, other_hp_delta=0, energy_req=0, self_energy_delta=0,
                 other_energy_delta=0, kills_req=0, metaclass=Singleton):
        self.description = description
        self.hp_req = hp_req
        self.self_hp_delta = self_hp_delta
        self.other_hp_delta = other_hp_delta
        self.energy_req = energy_req
        self.self_energy_delta = self_energy_delta
        self.other_energy_delta = other_energy_delta
        self.kills_req = kills_req

class Events:
    onepl = one_player_actions
    twopl = two_player_actions

    def get_random_1p_event(self, category):
        return self.onepl[category][randint(0, len(Events.onepl[category]) - 1)]

    def get_random_2p_event(self, category):
        return self.twopl[category][randint(0, len(Events.twopl[category]) - 1)]
